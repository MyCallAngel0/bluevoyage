from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, NotFound
from django.core.mail import send_mail
from .serializers import UserSerializer
from .models import User
import jwt
import datetime
import uuid
from django.conf import settings
from django.core.cache import cache
import pyotp
from django.views.decorators.csrf import csrf_exempt
from blogs.urls import get_user_blogs


class RegisterView(APIView):
    """API that manages signing up"""
    def post(self, request):
        # Gets the user information from client
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate and set the verification token
        user.verify_token = uuid.uuid4()

        # User will get its account unverified until they will access the verification link sent to their email
        user = User.objects.filter(email=request.data.get('email')).first()
        user.is_active = False
        user.save()

        self.send_verification_email(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def send_verification_email(self, user):
        # Creates a verification link using the token created above
        token = user.verify_token
        verification_link = f"http://localhost:3000/api/verify/{token}"  # Adjust this link as needed

        # Sends email with verification link to the user
        subject = 'Email Verification'
        message = f'Please verify your email by clicking the following link: {verification_link}'
        send_mail(subject, message, 'noreply@yourdomain.com', [user.email])


class VerifyEmailView(APIView):
    """API used for verifying your account after registering"""
    def get(self, request, token):
        try:
            # Account gets verified and user gets sent to login afterwards
            user = User.objects.get(verify_token=token)
            user.is_active = True
            user.verify_token = None
            user.save()
            return HttpResponse("""
                            <html>
                                <body>
                                    <h1>Email verified successfully!</h1>
                                    <p>Redirecting to login...</p>
                                    <script>
                                        setTimeout(function() {
                                            window.location.href = '/login';
                                        }, 3000);  // 3 second delay before redirecting
                                    </script>
                                </body>
                            </html>
                        """, content_type="text/html")

        except User.DoesNotExist:
            raise NotFound('User not found or token is invalid.')


class LoginView(APIView):
    """API that takes care of login"""
    def post(self, request):
        username = request.data.get('username')
        password = request.data['password']

        # Checks if you log in with email or username
        if '@' in username:
            user = User.objects.filter(email=username).first()
        else:
            user = User.objects.filter(username=username).first()

        # Validates the user
        if user is None:
            raise AuthenticationFailed("User not found!")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")

        # If the user didn't verify the account before logging in
        if not user.is_active:
            raise AuthenticationFailed("Account not verified!")

        # If you're an admin you can skip the OTP part
        if user.is_staff:
            payload = {
                'id': user.id,
                'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.now(datetime.timezone.utc)
            }

            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            user.last_login = datetime.datetime.now(datetime.timezone.utc)
            user.save()

            response = Response()
            response.set_cookie(key='jwt', value=token, httponly=True)
            response.data = {
                "jwt": token,
                "message": "Login successful"
            }

            return response

        # Creates an OTP that gets sent on your email
        otp, base32_secret = self.generate_otp()
        self.send_otp_email(user, otp)

        cache.set(f'otp_{user.id}', (otp, base32_secret), timeout=300)

        return Response({'message': 'OTP sent. Please check your email to complete login.'})

    # Method that generates the OTP
    def generate_otp(self):
        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret)
        otp = totp.now()

        return otp, secret

    # Method that sends the OTP to the user's email
    def send_otp_email(self, user, otp):
        subject = 'Your OTP for login'
        message = f'Your One-Time Password (OTP) is {otp}'
        email_from = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        send_mail(subject, message, email_from, recipient_list)


class VerifyOTPView(APIView):
    """API class used to verify the OTP"""
    def post(self, request):
        username = request.data['username']
        otp_provided = request.data['otp']

        # Checks if the user has logged in with email or username
        if '@' in username:
            user = User.objects.filter(email=username).first()
        else:
            user = User.objects.filter(username=username).first()

        # Validates user
        if not user:
            raise AuthenticationFailed("User not found.")

        # Gets the OTP from cache and compares it to the inserted OTP
        cached_otp, base32_secret = cache.get(f'otp_{user.id}', (None, None))
        if not cached_otp:
            raise AuthenticationFailed("OTP expired or not generated.")

        if not otp_provided == cached_otp:
            raise AuthenticationFailed("Invalid OTP.")

        # Creates a JWT token once the user inserts the correct OTP
        payload = {
            'id': user.id,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.now(datetime.timezone.utc)
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        user.last_login = datetime.datetime.now(datetime.timezone.utc)
        user.save()

        # Removes the OTP from the cache
        cache.delete(f'otp_{user.id}')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            "jwt": token,
            "message": "Login successful"
        }

        return response


class LogoutView(APIView):
    """API that logs the user out by removing the JWT token"""
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response


class UserView(APIView):
    """API that gets user data using the JWT token"""
    def get(self, request):
        token = request.COOKIES.get('jwt')

        # Validates and decodes token
        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Session expired!')

        # Searches for the user with the id taken from JWT token
        user = User.objects.filter(id=payload['id']).values('id', 'username', 'email', 'first_name', 'last_name').first()

        return Response(user)


class UserProfileView(APIView):
    """API that gets the profile page of a user"""
    @csrf_exempt
    def get(self, request, pk):
        user = (User.objects.filter(id=pk)
                .values('id', 'username', 'email', 'first_name', 'last_name', 'bio')
                .first())

        if not user:
            return Response({"error": "User not found"}, status=404)

        # Pass the pk to get_user_blogs function to retrieve blogs for this user
        blogs_data = get_user_blogs(request)

        user_profile = {
            "user": user,
            "blogs": blogs_data
        }

        return Response(user_profile)

    @csrf_exempt
    def put(self, request, pk):
        token = request.COOKIES.get('jwt')

        # Validates and decodes token
        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        # Verifies if the user id coincides with the user profile id
        if pk != payload['id']:
            return Response({"error": "Not authorized to edit this profile page!"}, status=status.HTTP_401_UNAUTHORIZED)

        updated_user = request.data

        user = User.objects.get(id=pk)
        if user is None:
            return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)
        user.first_name = updated_user.get('first_name', user.first_name)
        user.last_name = updated_user.get('last_name', user.last_name)
        user.bio = updated_user.get('bio', user.bio)
        user.save()

        return Response({"message: User profile updated successfully!"}, status=status.HTTP_202_ACCEPTED)


