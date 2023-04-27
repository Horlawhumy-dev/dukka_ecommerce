
from rest_framework import status
from rest_framework.test import APITestCase
from django.test import Client
from django.contrib.auth import get_user_model



class AuthTests(APITestCase):

    def setUp(self):
        self.client = Client()

        self.username = 'testuser'
        self.password = 'test@123'
        self.email = "test@test.co"
        self.first_name = "Testfirst"
        self.last_name = "Testlast"

        self.data = {
            "username": self.username,
            "password": self.password,
            "password2": self.password,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name
        }

        self.login_data = {
            "username": self.username,
            "password": self.password,
            "email": self.email
        }

    def test_register_endpoint(self):
        url = "/api/v1/auth/new/account"
        res = self.client.post(url, data=self.data, format="json")

        assert res.status_code == status.HTTP_200_OK #testcase status code

        res_json = res.json()
        assert res_json["status_code"] == status.HTTP_201_CREATED #status code from response
        assert res_json["data"]["is_active"] == True 

    
    def test_auth_endpoints(self):
        #save a test user for auth testcases
        user = get_user_model().objects.create_user(**self.login_data)
        user.is_active = True
        user.save()

        url = "/api/v1/token/"
        res = self.client.post(url, data=self.login_data, format="json")

        assert res.status_code == status.HTTP_200_OK #make sense since no user account was created
        access_token = res.json()["access"]
        assert len(access_token) > 10 #token length more than 10 characters

        url = "/api/v1/auth/account"
        headers = {"Authorization": f"Bearrer abc"} #wrong token
        res = self.client.get(url, headers=headers, format="json")

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

        headers = {"Authorization": f"Bearer {access_token}"}
        res = self.client.get(url, headers=headers, format="json")

        assert res.status_code == status.HTTP_200_OK