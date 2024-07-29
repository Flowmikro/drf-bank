from decimal import Decimal

from rest_framework import serializers

from bank_transaction.models import UserBalanceStoryModel


class BalanceStorySerializer(serializers.ModelSerializer):
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")

    class Meta:
        model = UserBalanceStoryModel
        fields = ('balance', 'transaction_date', 'type_balance',)


class BalanceSerializer(serializers.Serializer):
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0.01'))


class TransactionSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0.01'))
    recipient_id = serializers.IntegerField()

    def validate_amount(self, value):
        if 0 < value < 100:
            return value / 100
        return value
