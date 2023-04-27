
"""Payment Views"""
import logging
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import ChargeCardSerializer, OrderTransactionSerializer, \
	ValidateCardChargeSerializer, VerifyPaymentSerializer

from payment.models import Transaction
from account.views import APIResponse


UserModel = get_user_model()


class ChargeCardAPIView(APIView):
	"""View for charging card"""
	permission_classes = [IsAuthenticated]

	serializer_class = ChargeCardSerializer

	def post(self, request):
		"""Post method"""

		#no need of fullname in the request from user again
		request_user_fullname = f"{request.user.first_name} {request.user.last_name}"
		request.data["fullname"] = request_user_fullname

		serializer = self.serializer_class(data=request.data,  context={"request": request})
		if serializer.is_valid():
			response = serializer.charge_card()
			return Response(response.json(), status=response.status_code)
		else:
			return Response(serializer.errors, status=400)


class ValidateCardChargeAPIView(APIView):
	"""View for Validating Card Charge"""
	permission_classes = [IsAuthenticated]

	serializer_class = ValidateCardChargeSerializer


	def post(self, request):
		"""POST Request"""
		serializer = self.serializer_class(data=request.data,  context={"request": request})
		if serializer.is_valid():
			response = serializer.validate_charge()
			return Response(response.json(), status=response.status_code)
		else:
			return Response(serializer.errors, status=400)




class VerifyPaymentAPIView(APIView):
	"""View for Verifying Payment"""
	permission_classes = [IsAuthenticated]

	serializer_class = VerifyPaymentSerializer


	def post(self, request):
		"""POST Request"""
		serializer = self.serializer_class(data=request.data, context={"request": request})
		if serializer.is_valid():
			response = serializer.verify_payment()
			return Response(response.json(), status=response.status_code)
		else:
			return Response(serializer.errors, status=400)


class OrderTransaction(APIView):
	"""  View for Order Transaction Endpoint """
	permission_classes = [IsAuthenticated]

	def post(self, request):
		serializer = OrderTransactionSerializer(data=request.data, context={"request": request})

		if serializer.is_valid():

			serializer.save()

			return APIResponse.send(
				message=f"{request.user} order payment is successfully saved.",
				status=status.HTTP_201_CREATED,
				data=serializer.data
			)
		return APIResponse.send(
				message=f"Order transaction not saved.",
			status=status.HTTP_400_BAD_REQUEST,
			err=str(serializer.errors)
		)
	

	def get(self, request, *args, **kwargs):

		try:
			order_transactions = Transaction.objects.filter(user_involved=request.user)
		
		except Transaction.DoesNotExist as err:
			return APIResponse.send(
				message="Order transactions not found for this user.",
				status=status.HTTP_404_NOT_FOUND,
				err=str(err)
			)

		serializer = OrderTransactionSerializer

		if serializer.is_valid:

			data = serializer(order_transactions, many=True).data

			return APIResponse.send(
				message="Order transactions fetched successfully.",
				status=status.HTTP_200_OK,
				data=data
			)

		return APIResponse.send(
				message="Some serializer erros occurred.",
				status=status.HTTP_400_BAD_REQUEST,
				err=str(serializer.errors)
			)