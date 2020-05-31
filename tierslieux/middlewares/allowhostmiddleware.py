from django.conf import settings
from django import http
from django.utils.deprecation import MiddlewareMixin

class AllowHostsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        referer_url = request.META.get('HTTP_REFERER','')
        for allowed_referer in settings.ALLOWED_REFERER_URL:
            if referer_url.startswith(allowed_referer):
                return None
        return http.HttpResponseForbidden('<h1>Forbidden</h1>')