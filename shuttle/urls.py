from django.urls import path
from .views import CreateUserView, LoginView, GenerateOTPView, TransactionView

urlpatterns = [
    path('create/', CreateUserView.as_view()),
    path('login/', LoginView.as_view()),
    path('generate_otp/', GenerateOTPView.as_view()),
    path('transactions/', TransactionView.as_view(), name='transaction-list'),
]
