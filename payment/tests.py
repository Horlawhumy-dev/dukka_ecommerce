
from rest_framework import status
from rest_framework.test import APITestCase
from django.test import Client
from django.contrib.auth import get_user_model



class AuthPaymentTests(APITestCase):

    def setUp(self):
        self.client = Client()

        self.login_data = {
            "username": "testusername",
            "password": "testuser@123",
            "email": "test@testuser.co" #this won't be needed in login request
        }

        #these are all test data
        self.history_data = {
        "flutterwave_reference": "FLW-MOCK-cf74412998ded7fa569326b6dfb21c1c",
        "internal_reference": "DUKKA_2023_UCENWSHKYFSHZENT",
        "amount": 500,
        "card_type": "mastercard"
        }

    
    def test_history_payment_endpoints(self):
        #save a test user for payment history testcases
        user = get_user_model().objects.create_user(**self.login_data)
        user.is_active = True
        user.save()

        url = "/api/v1/token/"
        res = self.client.post(url, data=self.login_data, format="json")

        assert res.status_code == status.HTTP_200_OK #make sense since no user account was created
        access_token = res.json()["access"]
        assert len(access_token) > 10 #validating more than 10 characters for token

        #Testcase for wrong token
        url = "/api/v1/auth/account"
        headers = {"Authorization": f"Bearrer abc"} 
        res = self.client.get(url, headers=headers, format="json")

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

        headers = {"Authorization": f"Bearer {access_token}"}
        res = self.client.get(url, headers=headers, format="json")

        assert res.status_code == status.HTTP_200_OK

        url = "/api/v1/payment/order/history"
        headers = {"Authorization": f"Bearer {access_token}"}
        res = self.client.post(url, data=self.history_data, headers=headers, format="json")

        assert res.status_code == status.HTTP_200_OK

        assert res.json()["status_code"] == status.HTTP_201_CREATED

        url = "/api/v1/payment/order/history"
        headers = {"Authorization": f"Bearer {access_token}"}
        res = self.client.get(url, headers=headers, format="json")

        assert res.status_code == status.HTTP_200_OK

        assert res.json()["status_code"] == status.HTTP_200_OK

