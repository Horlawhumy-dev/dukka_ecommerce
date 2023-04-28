"""Payment Serializers"""

import random
import string
from datetime import datetime
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .wave import Flutterwave
from .models import Transaction

User = get_user_model()

class ChargeCardSerializer(serializers.Serializer):
	"""Serializer for collecting card details"""

	card_number = serializers.CharField(write_only=True)
	cvv = serializers.CharField(write_only=True)
	expiry_month = serializers.CharField(write_only=True)
	expiry_year = serializers.CharField(write_only=True)
	currency = serializers.CharField(default='NGN', write_only=True)
	amount = serializers.CharField(write_only=True)
	fullname = serializers.CharField(write_only=True)
	email = serializers.EmailField(write_only=True)
	pin = serializers.CharField(write_only=True)

	@staticmethod
	def get_transaction_reference(length=16):
		"""Generate Transaction Random String"""
		letters = string.ascii_lowercase
		random_str = ''.join(random.choice(letters) for i in range(length))
		dukka_transaction_reference = f'DUKKA_{datetime.now().year}_{random_str.upper()}'

		return dukka_transaction_reference
	
	def validate_email(self, value):
		request_user = self.context["request"].user

		if request_user.email != value:
			raise serializers.ValidationError("Email provided is not associated to request user performing transaction.")

		return value

	def charge_card(self):
		"""Charge Card"""
		self.is_valid(raise_exception=True)
		data = {
			"card_number": self.validated_data.get('card_number'),
			"cvv": self.validated_data.get('cvv'),
			"expiry_month": self.validated_data.get('expiry_month'),
			"expiry_year": self.validated_data.get('expiry_year'),
			"currency": self.validated_data.get('currency'),
			"amount": self.validated_data.get('amount'),
			"fullname": self.validated_data.get('fullname'),
			"email": self.validated_data.get('email'),
			"tx_ref": ChargeCardSerializer.get_transaction_reference(),
			"authorization": {
				"mode": "pin",
				"pin": self.validated_data.get('pin')
			}
		}
		flutterwave = Flutterwave()
		response = flutterwave.charge_card(data)
		return response

	def create(self, validated_data):
		"""Create Method"""
		pass

	def update(self, instance, validated_data):
		"""Update Method"""
		pass


class ValidateCardChargeSerializer(serializers.Serializer):
	"""Serializer for confirming payment"""

	otp = serializers.CharField()
	flw_ref = serializers.CharField()

	def validate_charge(self):
		"""Validate charge"""
		self.is_valid(raise_exception=True)
		flutterwave = Flutterwave()
		flw_ref = self.validated_data.get('flw_ref')
		otp = self.validated_data.get('otp')
		response = flutterwave.validate_charge(flw_ref, otp)
		return response

	def update(self, instance, validated_data):
		"""Update Method"""
		pass

	def create(self, validated_data):
		"""Create Method"""
		pass



class VerifyPaymentSerializer(serializers.Serializer):
	"""Serializer for Verifying payment"""

	transaction_id = serializers.CharField()

	def verify_payment(self):
		"""Verify Payment"""
		self.is_valid(raise_exception=True)
		flutterwave = Flutterwave()
		_id = self.validated_data.get('transaction_id')
		response = flutterwave.verify_transaction(_id)
		return response

	def update(self, instance, validated_data):
		"""Update Method"""
		pass

	def create(self, validated_data):
		"""Create Method"""
		pass


class OrderHistorySerializer(serializers.ModelSerializer):
	user_involved = serializers.SerializerMethodField()

	def get_user_involved(self, obj):
		return f"{obj.user_involved.first_name} {obj.user_involved.first_name}"
	

	class Meta:

		model = Transaction
		fields = "__all__"
		
	def create(self, validated_data):
		user = self.context["request"].user
		order_transaction = Transaction.objects.create(
		    flutterwave_reference=validated_data["flutterwave_reference"],
            internal_reference=validated_data["internal_reference"],
            amount=validated_data["amount"],
            card_type=validated_data["card_type"].upper(),
            user_involved=user
        )
		order_transaction.save()
		return order_transaction
	
	