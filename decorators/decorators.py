from django.http import HttpResponseRedirect
import jwt


def redirect_if_authenticated(redirect_url='/'):
    """Decorator used for restricting access to links where users don't need to access if they're authenticated"""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            token = request.COOKIES.get('jwt')

            if token:
                try:
                    jwt.decode(token, 'secret', algorithms=['HS256'])
                    return HttpResponseRedirect(redirect_url)
                except jwt.ExpiredSignatureError:
                    pass
                except jwt.InvalidTokenError:
                    pass

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator


def login_required(redirect_url='/login'):
    """Decorator used to restrict access to links where users need to be authenticated"""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            token = request.COOKIES.get('jwt')

            if token:
                try:
                    jwt.decode(token, 'secret', algorithms=['HS256'])
                    return view_func(request, *args, **kwargs)
                except jwt.ExpiredSignatureError:
                    return HttpResponseRedirect(redirect_url)
                except jwt.InvalidTokenError:
                    return HttpResponseRedirect(redirect_url)
            else:
                return HttpResponseRedirect(redirect_url)

        return wrapper

    return decorator
