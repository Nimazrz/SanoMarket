from django.http import JsonResponse

def simple_middleware(get_response):
    def middleware(request):
        if not request.user.is_active:
            return JsonResponse(
                {"detail": "اکانت شما در وضعیت غیر فعال قرار دارد"},
                status=401
            )

        response = get_response(request)
        return response

    return middleware
