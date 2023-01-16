from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from rest_framework import viewsets
from .serializers import StripeCheckoutSerializer
from rest_framework.views import APIView
from django.http import JsonResponse
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
webhook_secret = settings.STRIPE_WEBHOOK_SECRET

class StripeCheckoutViewSet(viewsets.ModelViewSet):
    serializer_class = StripeCheckoutSerializer
    http_method_names = ["post"]
    
    def create(self, request):
        validated_data = request.data
        try:
            checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": validated_data["price"],
                        "product_data": {
                            "name": validated_data["product_name"],
                            "images": [ validated_data["image"], ],
                        },
                    },
                    "quantity": validated_data["qty"], # quantity must be greater than 4
                },
            ],
            payment_method_types=['card',],
            mode='payment',
            success_url=settings.SITE_URL + '/payments/success/?success=true&session_id={CHECKOUT_SESSION_ID}',
            cancel_url=settings.SITE_URL + '/payments/cancel/?canceled=true',
            )
            return redirect(checkout_session.url)
        except Exception as e:
            return Response(
                {'error': e},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class WebHook(APIView):
    def post(self , request):
        event = None
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']

        try:
            event = stripe.Webhook.construct_event(
                payload ,sig_header , webhook_secret
                )
        except ValueError as err:
            # Invalid payload
            raise err
        except stripe.error.SignatureVerificationError as err:
            # Invalid signature
            raise err

        # Handle the event
        if event.type == 'payment_intent.succeeded':
            payment_intent = event.data.object 
            print("--------payment_intent ---------->" , payment_intent)
        elif event.type == 'payment_method.attached':
            payment_method = event.data.object 
            print("--------payment_method ---------->" , payment_method)
        # ... handle other event types
        else:
            print('Unhandled event type {}'.format(event.type))

        return JsonResponse(success=True, safe=False)

class SuccessView(APIView):
    def get(self, request):
        return Response({"message": "success"}, status=status.HTTP_200_OK)

class CancelView(APIView):
    def get(self, request):
        return Response({"message": "cancel"}, status=status.HTTP_200_OK)