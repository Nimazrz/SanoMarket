from django.http import JsonResponse


class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        print(request.user)
        print(not request.user.is_active)
        print(request.user.is_authenticated)

        response = self.get_response(request)

        return response
