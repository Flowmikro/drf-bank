from django.urls import path
from knox.views import LogoutView

from .views import LoginUserAPIView, RegisterAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginUserAPIView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
