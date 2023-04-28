"""URL patterns for Payments"""

from django.urls import path
from .views import ChargeCardAPIView, ValidateCardChargeAPIView, VerifyPaymentAPIView, OrderHistoryView

urlpatterns = [
    ############################# ENDPOINTS FOR PAYMENT PROVIDER #################
	path('charge/card', ChargeCardAPIView.as_view(), name="charge-card"),
	path('charge/validate', ValidateCardChargeAPIView.as_view(), name="charge-validate"),
    path('charge/verify', VerifyPaymentAPIView.as_view(), name="charge-verify"),
    
	############################# ENDPOINT FOR ORDER TRANSACTION #################
	path('order/history', OrderHistoryView.as_view(), name="order-history"),
]
