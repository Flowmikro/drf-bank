import logging
from decimal import Decimal

from django.db.models import F

from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from oauth.models import UserModel
from bank_transaction.text_choices import BalanceTypesChoices
from bank_transaction.models import UserBalanceStoryModel

logger = logging.getLogger(__name__)


def get_user_balance_story(user: UserModel):
    """
     Эта функция извлекает из базы данных историю баланса пользователя.
    """
    result = (
        UserBalanceStoryModel.objects.
        filter(user_id=user).
        select_related('user_id').
        values('balance', 'transaction_date', 'type_balance')
    )
    return result


def create_balance_story(user: UserModel, balance: Decimal, type_balance: BalanceTypesChoices) -> None:
    """
    Эта функция создает новую историю баланса в базе данных.

    Параметры:
    user (UserModel): Пользователь, для которого создается история баланса
    balance (Decimal): Сумма денег, задействованная в истории баланса
    type_balance (TypeBalance): Тип операции с балансом
    """
    try:
        UserBalanceStoryModel.objects.create(user_id=user, balance=balance, type_balance=type_balance)
    except Exception as e:
        logger.warning(f"Error creating Balance {str(e)}")


def update_user_balance(user_id: int, user: UserModel, balance: Decimal) -> None:
    """
    Эта функция обновляет баланс пользователя в базе данных, добавляя указанную сумму.
    Она также создает историю баланса в базе данных для записи транзакции.

    Параметры:
    user (UserModel): Пользователь, баланс которого необходимо обновить.
    balance (Decimal): Сумма, которая должна быть добавлена к балансу пользователя.

    """
    try:
        UserModel.objects.filter(id=user_id).update(balance=F('balance') + balance)
        create_balance_story(user=user, balance=balance, type_balance=BalanceTypesChoices.RECEIVED_TRANSFER)

    except Exception as e:
        logger.warning(f'Error {str(e)}')


def transfer_money(user: UserModel, amount: Decimal, recipient_id: int) -> None:
    """
    Эта функция переводит указанную сумму денег со счета отправителя на счет получателя.
    Она также создает истории баланса в базе данных для отправителя и получателя.

    Параметры:
    user (UserModel): Объект модели пользователя отправителя
    amount (Decimal): Сумма денег для перевода
    recipient_id (int): Идентификатор объекта пользовательской модели получателя
    """
    recipient = get_object_or_404(UserModel, id=recipient_id)
    try:
        user.balance -= amount
        create_balance_story(user=user, balance=user.balance, type_balance=BalanceTypesChoices.MADE_TRANSFER)
        recipient.balance += amount
        create_balance_story(user=recipient, balance=recipient.balance,
                             type_balance=BalanceTypesChoices.RECEIVED_TRANSFER)
        user.save(update_fields=['balance'])
        recipient.save(update_fields=['balance'])
    except Exception as e:
        logger.warning(f'Error {str(e)}')


def get_user_balance(user_id) -> Response:
    """
    Эта функция извлекает баланс пользователя из базы данных.

    Параметры:
    user_id (int): Уникальный идентификатор пользователя, баланс которого необходимо получить.
    """
    user = UserModel.objects.filter(id=user_id).values('balance').first()
    if user is None:
        return Response(
            {
                'Message': 'User not found'
            },
            status=status.HTTP_404_NOT_FOUND
        )
    return user
