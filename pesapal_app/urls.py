from django.urls import path
from .views import *

urlpatterns = [
    path('pesapal-callback/', pesapal_callback),
]