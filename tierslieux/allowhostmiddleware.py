from django.conf import settings
from django import http
from django.utils.deprecation import MiddlewareMixin

class AllowHostsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        referer_url = request.META.get('HTTP_REFERER','')
        if referer_url.startswith(settings.ALLOWED_REFERER_URL):
            return None
        return http.HttpResponseForbidden('<h1>Forbidden</h1>')