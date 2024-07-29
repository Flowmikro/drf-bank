from django.urls import path

from .views import IncreaseBalanceAPIView, TransferMoneyAPIView, GetUserBalanceAPIView, BalanceHistoryListAPIView

urlpatterns = [
    path('increase-balance/', IncreaseBalanceAPIView.as_view(), name='increase_balance'),
    path('transfer-money/', TransferMoneyAPIView.as_view(), name='transfer_money'),
    path('user-balance/', GetUserBalanceAPIView.as_view(), name='user_balance'),
    path('balance-history/', BalanceHistoryListAPIView.as_view(), name='balance_history'),
]
