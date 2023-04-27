import logging
from django.db import models
from django.contrib.auth import get_user_model
from .choices import *

User = get_user_model()


class Transaction(models.Model):
	"""Order Transaction History model"""

	flutterwave_reference = models.CharField(max_length=64, blank=True, null=True)
	internal_reference = models.CharField(max_length=64, blank=True, null=True)
	amount = models.DecimalField(max_digits=16, decimal_places=2, blank=False, default=0.00)
	date = models.DateTimeField(auto_now_add=True)
	transaction_type = models.CharField(max_length=64, default=DEFAULT_TRANSACTION_TYPE, blank=True, null=True)
	card_type = models.CharField(
		max_length=16,
		default=DEFAULT_CARD_TYPE,
		choices=card_type_choices
	)
	user_involved = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_transaction")

	def __str__(self):
		return self.internal_reference