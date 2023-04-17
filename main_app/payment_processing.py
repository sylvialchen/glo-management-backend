from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
import stripe
import json
import environ

env = environ.Env()
environ.Env.read_env()

stripe.api_key = env("STRIPE_API_KEY")

@csrf_exempt
def create_payment_intent(request, *args, **kwargs):
    print(request.body)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(f"Data received: {data}")
        except json.JSONDecodeError:
            return HttpResponseBadRequest('Invalid JSON data')
        try:
            intent = stripe.PaymentIntent.create(
                amount=1000,
                currency='usd',
                payment_method_types=['card']
            )
            print(f"PaymentIntent created: {intent.id}")
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            print(f"Error creating PaymentIntent: {e}")
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)
