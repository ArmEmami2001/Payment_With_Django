from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController
from creditpurchase.controller import ShopController,Registration,ProfileController

api = NinjaExtraAPI(
    title="My Project API (with Controllers)",
    version="1.0.0",
)

api.register_controllers(NinjaJWTDefaultController)
api.register_controllers(Registration)
api.register_controllers(ShopController)
api.register_controllers(ProfileController)
