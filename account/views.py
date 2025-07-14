from django.contrib.auth import logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated
import redis
from rest_framework_simplejwt.tokens import RefreshToken
import secrets
import uuid


def send_sms(phone):
    if CustomUser.objects.filter(phone=phone).exists():
        code = secrets.randbelow(9000) + 1000
        print(f"Sending code {code} to phone {phone}")
        return code
    return False


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignupAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    """
    {
    "X-CSRFToken":"{% csrf_tocken %}"
    }
    """

    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response({"message": "you have logged out succesfully"}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# redis-server
r = redis.Redis(host='localhost', port=6379, db=0)


class SigninView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = SigninSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']

            if r.exists(f'verify_{phone}'):
                return Response({"message": "Your code has been sent already"}, status=200)

            code = send_sms(phone)
            if not code:
                return Response({"message": "You have not signed up"}, status=400)

            temp_id = str(uuid.uuid4())
            r.hset(f'verify_{temp_id}', mapping={"phone": phone, 'code': str(code)})
            r.expire(f'verify_{temp_id}', 120)
            return Response({"message": "The code has been sent",
                             "verify_token": temp_id},
                            status=200)

        return Response(serializer.errors, status=400)


class VerifyCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data['code']
            verify_token = serializer.validated_data['verify_token']

            if not verify_token:
                return Response({"message": "token has not been sent! try again."}, status=400)

            if not r.exists(f'verify_{verify_token}'):
                return Response({"message": "Code does not exist or expired"}, status=400)

            redis_code = r.hget(f'verify_{verify_token}', "code")
            redis_phone = r.hget(f'verify_{verify_token}', "phone")
            if redis_code and redis_code.decode() == str(code):
                try:
                    user = CustomUser.objects.get(phone= redis_phone.decode())

                except CustomUser.DoesNotExist:
                    return Response({"message": "User not found"}, status=404)

                refresh = RefreshToken.for_user(user)
                access = refresh.access_token
                r.delete(f'verify_{verify_token}')
                return Response({
                    "message": "Code verified",
                    "access": str(access),
                    "refresh": str(refresh)
                }, status=200)
            else:
                return Response({"message": "Wrong code"}, status=400)
        return Response(serializer.errors, status=400)
