from django.http import HttpResponsePermanentRedirect


class WwwRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().partition(':')[0]
        if host == "http://www.nodewe.com" or "https://www.nodewe.com":
            return HttpResponsePermanentRedirect(
                "http://nodewe.com" + request.path
            )
        else:
            return self.get_response(request)
