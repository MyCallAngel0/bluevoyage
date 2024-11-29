import time
from django.core.cache import cache
from django.http import JsonResponse

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)
        key = f"rate-limit-{ip}"
        requests = cache.get(key, 0)

        if requests >= 10:  # Limit: 10 requests per minute
            return JsonResponse({'error': 'Too many requests'}, status=429)

        cache.set(key, requests + 1, timeout=60)  # Reset count every minute
        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
