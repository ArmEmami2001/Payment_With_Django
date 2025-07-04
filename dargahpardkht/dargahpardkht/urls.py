from django.contrib import admin
from django.urls import path, include
from .api import api
from azbankgateways.urls import az_bank_gateways_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls), 
    path('bankgateways/',az_bank_gateways_urls()),
    ]