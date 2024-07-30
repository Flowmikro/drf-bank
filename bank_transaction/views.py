from decimal import Decimal

from django.db import transaction

from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from bank_transaction.models import UserBalanceStoryModel
from bank_transaction import serializers
from bank_transaction import services


class BalanceHistoryListAPIView(ListAPIView):
    """
    Класс для получения списка истории баланса пользователя
    """
    model = UserBalanceStoryModel
    serializer_class = serializers.BalanceStorySerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        return services.get_user_balance_story(user=user)


class GetUserBalanceAPIView(APIView):
    """
    Возвращает баланс пользователя
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = serializers.BalanceSerializer

    def get(self, request, *args, **kwargs) -> Response:
        # Получаем текущий баланс пользователя
        user_balance = services.get_user_balance(user_id=self.request.user.id)

        return Response(
            data=user_balance,
        )


class IncreaseBalanceAPIView(APIView):
    """
    Класс для увеличения баланса пользователя.
    """

    serializer_class = serializers.BalanceSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs) -> Response:
        try:
            # Получаем данные запроса
            balance = Decimal(self.request.data['balance'])
            if balance <= 0:
                return Response(
                    data={
                        'Message': 'The amount should be greater than 0'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Запускаем задачу для увеличения баланса
            with transaction.atomic():
                services.update_user_balance(
                    user_id=self.request.user.id,
                    user=self.request.user,
                    balance=balance,
                )

            return Response(
                {
                    'Message': 'Balance successfully increased',
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {
                    'Error': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TransferMoneyAPIView(APIView):
    """
    Трансфер денег
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = serializers.TransactionSerializer

    def post(self, request, *args, **kwargs) -> Response:
        try:
            # Получаем данные запроса
            data = self.request.data
            amount = Decimal(data['amount'])
            recipient_id = data['recipient_id']

            if amount <= 0:
                return Response(
                    data={
                        'Message': 'The amount should be greater than 0'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Получаем текущий баланс пользователя
            user_balance = services.get_user_balance(user_id=self.request.user.id)
            current_balance = user_balance['balance']

            # Проверяем, достаточно ли денег на балансе
            if current_balance < amount:
                return Response(
                    {
                        'Message': 'Not enough money on the balance'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            if self.request.user.id == recipient_id:
                return Response(
                    data={
                        "Message": "You can't translate to yourself"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            with transaction.atomic():
                services.transfer_money(
                    user=self.request.user,
                    amount=amount,
                    recipient_id=recipient_id
                )

            return Response(
                data={
                    'Message': 'The money has been transferred'
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                data={
                    'Error': f'{str(e)}',
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
