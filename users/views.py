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


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        user = User.objects.filter(email=request.data.get('email')).first()
        user.is_active = False
        user.verify_token = uuid.uuid4()
        user.save()

        self.send_verification_email(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def send_verification_email(self, user):
        token = user.verify_token
        verification_link = f"127.0.0.1:8000/api/verify/{token}"  # Adjust this link as needed

        subject = 'Email Verification'
        message = f'Please verify your email by clicking the following link: {verification_link}'
        send_mail(subject, message, 'noreply@yourdomain.com', [user.email])


class VerifyEmailView(APIView):
    def get(self, request, token):
        try:
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
    def post(self, request):
        username = request.data.get('username')
        password = request.data['password']

        if '@' in username:
            user = User.objects.filter(email=username).first()
        else:
            user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed("User not found!")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")

        if not user.is_active:
            raise AuthenticationFailed("Account not verified!")

        if user.is_staff:
            payload = {
                'id': user.id,
                'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.now(datetime.UTC)
            }

            token = jwt.encode(payload, 'secret', algorithm='HS256')
            user.last_login = datetime.datetime.now(datetime.UTC)
            user.save()

            response = Response()
            response.set_cookie(key='jwt', value=token, httponly=True)
            response.data = {
                "jwt": token,
                "message": "Login successful"
            }

            return response

        otp, base32_secret = self.generate_otp()
        self.send_otp_email(user, otp)

        cache.set(f'otp_{user.id}', (otp, base32_secret), timeout=300)

        return Response({'message': 'OTP sent. Please check your email to complete login.'})

    def generate_otp(self):
        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret)
        otp = totp.now()

        return otp, secret

    def send_otp_email(self, user, otp):
        subject = 'Your OTP for login'
        message = f'Your One-Time Password (OTP) is {otp}'
        email_from = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        send_mail(subject, message, email_from, recipient_list)


class VerifyOTPView(APIView):
    def post(self, request):
        username = request.data['username']
        otp_provided = request.data['otp']

        user = User.objects.filter(username=username).first()

        if not user:
            raise AuthenticationFailed("User not found.")

        cached_otp, base32_secret = cache.get(f'otp_{user.id}', (None, None))

        if not cached_otp:
            raise AuthenticationFailed("OTP expired or not generated.")

        if not otp_provided == cached_otp:
            raise AuthenticationFailed("Invalid OTP.")

        payload = {
            'id': user.id,
            'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.now(datetime.UTC)
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        user.last_login = datetime.datetime.now(datetime.UTC)
        user.save()

        cache.delete(f'otp_{user.id}')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            "jwt": token,
            "message": "Login successful"
        }

        return response


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)
