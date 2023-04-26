from __future__ import absolute_import, unicode_literals
import os
import random
import string
from datetime import datetime
from .wave import Flutterwave

from celery import shared_task

@shared_task(name = "charge_customer")
def charge_customer(message, *args, **kwargs):
    charge_response = charge_card()
    validate_response = validate_charge(charge_response)

    verify_payment(validate_response)
  

def get_transaction_reference(length=16):
    """Generate Transaction Random String"""
    letters = string.ascii_lowercase
    random_str = ''.join(random.choice(letters) for i in range(length))
    dukka_transaction_reference = f'DUKKA_{datetime.now().year}_{random_str.upper()}'

    return dukka_transaction_reference


def charge_card():
    """Charge Card"""
    data = {
        "card_number": str(os.getenv("CARD_NUMBER")),
        "cvv": str(os.getenv("CVV")),
        "expiry_month": str(os.getenv("EXPIRY_MONTH")),
        "expiry_year": str(os.getenv("EXPIRY_YEAR")),
        "currency": str(os.getenv("CURRENCY")),
        "amount": str(os.getenv("AMOUN")),
        "fullname": str(os.getenv("FULLNAME")),
        "email": str(os.getenv("EMAIL")),
        "tx_ref": get_transaction_reference(),
        "authorization": {
            "mode": "pin",
            "pin": str(os.getenv("PIN"))
        }
    }
    flutterwave = Flutterwave()
    response = flutterwave.charge_card(data)
    return response

def validate_charge(response:  dict()):
    """Validate charge"""
    flw_ref = response["data"]["flw_ref"]
    otp = str(os.getenv["OTP"])
    flutterwave = Flutterwave()
    response = flutterwave.validate_charge(flw_ref, otp)
    return response

def verify_payment(response: dict()):
    """Verify Payment"""
    _id = response["data"]['transaction_id']
    flutterwave = Flutterwave()
    response = flutterwave.verify_transaction(_id)
    return response
