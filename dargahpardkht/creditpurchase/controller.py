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
    @route.get("/purchase-credits")
    def purchase_credits(self, request: HttpRequest, amount: int = 1000000000):
        user_mobile_number="+989171111111"
        factory=bankfactories.BankFactory()
        try:
            bank=(
                factory.auto_create()
                )
            bank.set_amount(amount)
            bank.set_request(request)
            bank.set_custom_data({"a":"b"})
            bank.set_client_callback_url("http://127.0.0.1:8000/api/shop/")
            bank_record=bank.ready()
            print(bank_record)
            redirect_object = bank.redirect_gateway()
            
            # 2. Extract the URL string from that object's .url attribute
            redirect_url_string = redirect_object.url
            
            # 3. Return the URL string in a clean JSON response
            return self.api.create_response(request, {"redirect_url": redirect_url_string}, status=200)
        except AZBankGatewaysException as e:
            logging.critical(e)
            raise e
        
    @route.get("/")
    def check_payment_status(self, request: HttpRequest, tc: str):
        user = request.auth
        user_profile = get_object_or_404(UserProfile, user=user)

        try:
            bank_record = get_object_or_404(
                bank_models.Bank, tracking_code=tc,reference_number=user_profile.id
            )
            if bank_record.is_success:
                
                credits_to_add = bank_record.amount / 100
                user_profile.credits += credits_to_add
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
        