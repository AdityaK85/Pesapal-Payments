from django.shortcuts import render
from django.http import JsonResponse
from Pesapal_Integrations.pesapal_payments import transaction_status, transaction_status_by_api

# Create your views here.


'''
This Django project only created for show the response after making payment 
1. Add local server redirect url of this django project 
2. Run pesapal_payments python file & after payment can redirect this django local server as a redirect url

API Reference:
https://documenter.getpostman.com/view/6715320/UyxepTv1#db9b2776-c795-485c-a6cf-9ecb15fc8c71

Test Payment Card :
https://cybqa.pesapal.com/PesapalIframe/PesapalIframe3/TestPayments
'''


def pesapal_callback(request):
    order_tracking_id = request.GET.get('OrderTrackingId')
    url_res = transaction_status_by_api(order_tracking_id)
    return render(request, 'index.html', {'response':url_res})