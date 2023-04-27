from __future__ import absolute_import, unicode_literals
import os
import random
import string
from datetime import datetime
from .wave import Flutterwave

from celery import shared_task

flutterwave = Flutterwave()


@shared_task(name = "charge_customer")
def charge_customer():
    verify_res = verify_payment()
    print(verify_res) #printing the response for testing only
  

def get_transaction_reference(length=16):
    """Generate Transaction Random String"""
    letters = string.ascii_lowercase
    random_str = ''.join(random.choice(letters) for i in range(length))
    dukka_transaction_reference = f'DUKKA_{datetime.now().year}_{random_str.upper()}'

    return dukka_transaction_reference


def charge_card():
    """Charge Card"""
    #ofcourse this credential would be cached in a more secure way 
    data = {
        "card_number": str(os.getenv("CARD_NUMBER")),
        "cvv": str(os.getenv("CVV")),
        "expiry_month": str(os.getenv("EXPIRY_MONTH")),
        "expiry_year": str(os.getenv("EXPIRY_YEAR")),
        "currency": str(os.getenv("CURRENCY")),
        "amount": str(os.getenv("AMOUNT")),
        "fullname": str(os.getenv("FULLNAME")),
        "email": str(os.getenv("EMAIL")),
        "tx_ref": get_transaction_reference(),
        "authorization": {
            "mode": "pin",
            "pin": str(os.getenv("PIN"))
        }
    }
    res = flutterwave.charge_card(data)
    return res.json()

def validate_charge():
    """Validate charge"""
    response = charge_card()
    flw_ref = response["data"]["flw_ref"]
    otp = "6656" #str(os.getenv["OTP"])
    res = flutterwave.validate_charge(flw_ref, otp)
    return res.json()

def verify_payment():
    """Verify Payment"""
    response = validate_charge()
    _id = response["data"]["id"]
    res = flutterwave.verify_transaction(_id)
    return res.json()
