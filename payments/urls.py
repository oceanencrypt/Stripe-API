from rest_framework import routers
from .views import StripeCheckoutViewSet, WebHook, SuccessView, CancelView
from django.urls import path

router = routers.SimpleRouter()
router.register(r'create-checkout-session', StripeCheckoutViewSet, basename="stripe-checkout")
urlpatterns = [
    path("webhook/",  WebHook.as_view()),
    path("success/",  SuccessView.as_view(), name="success"),
    path("cancel/",  CancelView.as_view(), name="cancel"),
]

urlpatterns += router.urls