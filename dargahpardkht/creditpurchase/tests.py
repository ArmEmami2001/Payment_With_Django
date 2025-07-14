import unittest.mock
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from ninja.testing import TestClient
from dargahpardkht.api import api
from .models import UserProfile
from azbankgateways import models as bank_models


User = get_user_model()
client = TestClient(api)  # Create once, outside the class

class RegistrationAndAuthTests(TestCase):
    def setUp(self):
        self.client = client

    @patch('dargahpardkht.urls.az_bank_gateways_urls')
    def test_create_user_success(self, _):
        user_data = {"username": "testuser", "email": "test@example.com", "password": "complexpassword123"}
        response = self.client.post("/register/create_user", json=user_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username="testuser").exists())
        user_profile = UserProfile.objects.get(user__username="testuser")
        self.assertEqual(user_profile.credits, 1)
        response_data = response.json()
        self.assertEqual(response_data["username"], "testuser")
        self.assertEqual(response_data["credits"], 1)

    @patch('dargahpardkht.urls.az_bank_gateways_urls')
    def test_get_jwt_token_success(self, _):
        user_data = {"username": "loginuser", "password": "password123"}
        User.objects.create_user(**user_data)
        response = self.client.post("/token/pair", json=user_data)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("access", response_data)
        self.assertIn("refresh", response_data)


# class ProfileAndShopTests(TestCase):
#     def setUp(self):

#         self.user = User.objects.create_user(username="shopuser", password="shoppassword")
#         self.profile = UserProfile.objects.create(user=self.user, credits=100)
#         login_data = {"username": "shopuser", "password": "shoppassword"}
#         client = TestClient(api) 
#         response = client.post("/token/pair", json=login_data)
#         self.token = response.json()["access"]
#         self.client = TestClient(api, headers={"Authorization": f"Bearer {self.token}"})

#     def test_get_profile_success(self):
    
#         response = self.client.get("/profile/")
#         self.assertEqual(response.status_code, 200)
#         expected_data = {"username": "shopuser", "credits": 100}
#         self.assertEqual(response.json(), expected_data)

#     @unittest.mock.patch('creditpurchase.controller.bankfactories.BankFactory.auto_create')
#     def test_purchase_credits_success(self, mock_auto_create):
    
#         mock_bank = unittest.mock.MagicMock()
#         mock_bank.ready.return_value = bank_models.Bank.objects.create(amount=50000)
#         mock_bank.redirect_gateway.return_value = unittest.mock.Mock(url="https://sandbox.zarinpal.com/pg/StartPay/MOCKED_URL")
#         mock_auto_create.return_value = mock_bank
#         response = self.client.get("/shop/purchase-credits?amount=50000")
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("redirect_url", response.json())
#         self.assertEqual(response.json()["redirect_url"], "https://sandbox.zarinpal.com/pg/StartPay/MOCKED_URL")

#     def test_verify_payment_success(self):
#         bank_record = bank_models.Bank.objects.create(
#             amount="500000",
#             tracking_code="test_tracking_code",
#             is_success=True,
#             extra_information="0"
#         )
#         response = self.client.get(f"/shop/verify-payment?tc={bank_record.tracking_code}")
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json()["message"], "Payment successful and credits added.")
#         self.profile.refresh_from_db()
#         self.assertEqual(self.profile.credits, 100 + 500)
#         bank_record.refresh_from_db()
#         self.assertEqual(bank_record.extra_information, "1")

#     def test_verify_payment_already_processed(self):
     
#         bank_record = bank_models.Bank.objects.create(
#             amount="500000",
#             tracking_code="already_processed_tc",
#             is_success=True,
#             extra_information="1" 
#         )

   
#         response = self.client.get(f"/shop/verify-payment?tc={bank_record.tracking_code}")
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json()["message"], "Already Added")
#         self.profile.refresh_from_db()
#         self.assertEqual(self.profile.credits, 100) 