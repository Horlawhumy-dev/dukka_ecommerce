"""URL patterns for Payments"""

from django.urls import path
from .views import ChargeCardAPIView, ValidateCardChargeAPIView, VerifyPaymentAPIView, OrderTransaction

urlpatterns = [
    ############################# ENDPOINTS FOR PAYMENT PROVIDER #################
	path('charge/card', ChargeCardAPIView.as_view()),
	path('charge/validate', ValidateCardChargeAPIView.as_view()),
    path('charge/verify', VerifyPaymentAPIView.as_view()),
    
	############################# ENDPOINT FOR ORDER TRANSACTION #################
	path('order/receipt', OrderTransaction.as_view(), name="oder-payment"),
]
