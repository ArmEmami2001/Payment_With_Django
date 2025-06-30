from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja_extra import api_controller, route
from ninja_jwt.authentication import JWTAuth
from azbankgateways import bankfactories, models as bank_models, exceptions as bank_exceptions
from .models import UserProfile
from .schema import UserCreateSchema,UserReadSchema
from django.db import transaction
from django.contrib.auth import get_user_model

User = get_user_model()


@api_controller("/shop", auth=JWTAuth(), tags=['shop'])
class ShopController:
    @route.post("/purchase-credits")
    def purchase_credits(self, request: HttpRequest, amount: int = 10000):
        user = request.auth
        user_profile = get_object_or_404(UserProfile, user=user)

        factory = bankfactories.BankFactory()
        try:
            bank = factory.auto_create()
            bank.set_request(request)
            bank.set_amount(amount)
            bank.set_client_callback_url('/bankgateways/callback/')
            bank.set_reference_number(user_profile.id)
            bank_record = bank.ready()
            return {"redirect_url": bank.redirect_gateway()}
        except bank_exceptions.BankGatewayException as e:
            return {"error": str(e)}

    @route.get("/check-payment-status")
    def check_payment_status(self, request: HttpRequest, tracking_code: str):
        user = request.auth
        user_profile = get_object_or_404(UserProfile, user=user)

        try:
            bank_record = get_object_or_404(
                bank_models.Bank, tracking_code=tracking_code, reference_number=user_profile.id
            )
            if bank_record.is_success:
                if not bank_record.is_completed():
                    credits_to_add = bank_record.amount / 100
                    user_profile.credits += credits_to_add
                    user_profile.save()
                    bank_record.set_as_completed()
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
        return user