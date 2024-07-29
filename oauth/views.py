import logging

from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from knox.models import AuthToken

from oauth import serializers
from oauth.models import UserModel

logger = logging.getLogger(__name__)


class RegisterAPIView(CreateAPIView):
    serializer_class = serializers.UserCreateSerializer
    permission_classes = [AllowAny, ]
    model = UserModel


class LoginUserAPIView(GenericAPIView):
    serializer_class = serializers.LoginUserSerializer
    permission_classes = [AllowAny, ]

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data
            return Response({
                "token": AuthToken.objects.create(user)[1]
            })
        except Exception as err:
            logging.warning(f'Error {type(err).__name__}'),
            return Response(
                data={
                    'Error': 'Server-side error'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
