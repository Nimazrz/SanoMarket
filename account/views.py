from django.contrib.auth import logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import SignupSerializer


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
