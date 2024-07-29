from django.db import models

from oauth.models import UserModel
from bank_transaction.text_choices import BalanceTypesChoices


class UserBalanceStoryModel(models.Model):
    user_id = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=20, decimal_places=10)
    transaction_date = models.DateTimeField(auto_now_add=True)
    type_balance = models.CharField(max_length=50, choices=BalanceTypesChoices.choices, default=BalanceTypesChoices.MADE_TRANSFER)

    def __str__(self):
        return f'User: {self.user_id}, Balance: {self.balance},  Transaction Date: {self.transaction_date}'
