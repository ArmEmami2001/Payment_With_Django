from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja_extra import api_controller, route
from ninja_jwt.authentication import JWTAuth
from azbankgateways import bankfactories, models as bank_models, exceptions as bank_exceptions
from .models import UserProfile
from .schema import UserCreateSchema,UserReadSchema
from django.db import transaction
from django.contrib.auth import get_user_model
import logging
import time
from django.urls import reverse
from azbankgateways.exceptions import AZBankGatewaysException

User = get_user_model()
logger = logging.getLogger(__name__)


@api_controller("/shop", auth=JWTAuth(), tags=['shop'])
class ShopController:
    @route.get("/purchase-credits",auth=JWTAuth())
    def purchase_credits(self, request: HttpRequest, amount: int = 100000):
        user_mobile_number="+989171111111"
        user = request.auth 
        user_profile = get_object_or_404(UserProfile, user=user)
        factory=bankfactories.BankFactory()
        try:
            bank=(
                factory.auto_create()
                )

            bank.set_amount(amount)
            bank.set_request(request)
            bank.set_custom_data({"a":"b"}) 
            bank.set_client_callback_url("http://localhost:5500/index.html?tc={tracking_code}")
            bank_record=bank.ready()
            redirect_object = bank.redirect_gateway()
            redirect_url_string = redirect_object.url
            return self.api.create_response(request, {"redirect_url": redirect_url_string}, status=200)
        except AZBankGatewaysException as e:
            logging.critical(e)
            raise e
    # @route.get("/purchase-20credits",auth=JWTAuth())
    # def purchase_credits(self, request: HttpRequest, amount: int = 200000):
    #     user_mobile_number="+989171111111"
    #     user = request.auth 
    #     user_profile = get_object_or_404(UserProfile, user=user)
    #     factory=bankfactories.BankFactory()
    #     try:
    #         bank=(
    #             factory.auto_create()
    #             )

    #         bank.set_amount(amount)
    #         bank.set_request(request)
    #         bank.set_custom_data({"a":"b"}) 
    #         bank.set_client_callback_url("http://localhost:5500/index.html?tc={tracking_code}")
    #         bank_record=bank.ready()
    #         redirect_object = bank.redirect_gateway()
    #         redirect_url_string = redirect_object.url
    #         return self.api.create_response(request, {"redirect_url": redirect_url_string}, status=200)
    #     except AZBankGatewaysException as e:
    #         logging.critical(e)
    #         raise e
        
    @route.get("/verify-payment")
    def check_payment_status(self, request: HttpRequest, tc: str):
        user = request.auth
        user_profile = get_object_or_404(UserProfile, user=user)

        try:
            
            bank_record = get_object_or_404(
                bank_models.Bank, tracking_code=tc )
            
            if bank_record.is_success:
                
                credits_to_add = int(bank_record.amount)/1000
                user_profile.credits += int(credits_to_add)
                user_profile.save()
                return {"status": "success", "message": "Payment successful and credits added."}
            else:
                return {"status": "failed", "message": bank_record.get_message()}
        except bank_models.Bank.DoesNotExist:
            return {"status": "error", "message": "Transaction not found."}
        
@api_controller("/register")
class Registration:
    @route.post("/create_user", response=UserReadSchema)
    def create(self, request, payload: UserCreateSchema):
        with transaction.atomic():
            user = User.objects.create_user(
                username=payload.username,
                email=payload.email,
                password=payload.password,
            )
            UserProfile.objects.create(user=user, credits=1)
            return {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "credits": user.profile.credits,  
            }
@api_controller("/profile", auth=JWTAuth())
class ProfileController:
    @route.get("/")
    def get_profile(self, request):
        return {
            "username": request.auth.username,
            "credits": request.auth.profile.credits,
        }
