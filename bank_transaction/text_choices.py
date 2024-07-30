from django.db.models import TextChoices


class BalanceTypesChoices(TextChoices):
    RECEIVED_TRANSFER = 'Вам перевели деньги'
    MADE_TRANSFER = 'Вы перевели деньги'
    ACCOUNT_RECHARGED = 'Вы пополнили свой счет'
