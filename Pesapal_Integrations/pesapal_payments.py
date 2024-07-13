import requests
import json

# Live
# url = 'https://pay.pesapal.com/v3/api/'
# Test
base_url = 'https://cybqa.pesapal.com/pesapalv3/api/'

consumer_key = 'ngW+UEcnDhltUc5fxPfrCD987xMh3Lx8'
consumer_secret = 'q27RChYs5UkypdcNYKzuUw460Dg='

Token = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3VzZXJkYXRhIjoiNzJjMjZkYzAtYTBjZS00ZjUxLWE4NjItZTA0MzQ1NjE3MzU2IiwidWlkIjoibmdXK1VFY25EaGx0VWM1ZnhQZnJDRDk4N3hNaDNMeDgiLCJuYmYiOjE3MjA4Nzc2NDEsImV4cCI6MTcyMDg4MTI0MSwiaWF0IjoxNzIwODc3NjQxLCJpc3MiOiJodHRwOi8vY3licWEucGVzYXBhbC5jb20vIiwiYXVkIjoiaHR0cDovL2N5YnFhLnBlc2FwYWwuY29tLyJ9.udi2r9hnHM84RQI8clCQy3PpRT0mEae0StoZQNz9Ms8'

def access_token():
    global Token

    url = f'{base_url}Auth/RequestToken'

    payload = json.dumps({
        "consumer_key": consumer_key,
        "consumer_secret": consumer_secret
        })
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
        }

    response = requests.request("POST", url, headers=headers, data=payload)
    response =  response.json()
    if response['status'] == "200":
        Token = response['token']
    return response

'''
Response:
{'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3VzZXJkYXRhIjoiNzJjMjZkYzAtYTBjZS00ZjUxLWE4NjItZTA0MzQ1NjE3MzU2IiwidWlkIjoibmdXK1VFY25EaGx0VWM1ZnhQZnJDRDk4N3hNaDNMeDgiLCJuYmYiOjE3MjA4Nzc2NDEsImV4cCI6MTcyMDg4MTI0MSwiaWF0IjoxNzIwODc3NjQxLCJpc3MiOiJodHRwOi8vY3licWEucGVzYXBhbC5jb20vIiwiYXVkIjoiaHR0cDovL2N5YnFhLnBlc2FwYWwuY29tLyJ9.udi2r9hnHM84RQI8clCQy3PpRT0mEae0StoZQNz9Ms8', 'expiryDate': '2024-07-13T14:34:01.7987035Z', 'error': None, 'status': '200', 'message': 'Request processed successfully'}
'''


# print(access_token())

def register_ipn_url():

    url = f'{base_url}URLSetup/RegisterIPN'

    payload = json.dumps({
        "url": "http://127.0.0.0.1:8000/test-mode/python/",
        "ipn_notification_type": "POST"
        })

    headers = {
    'Authorization': Token,
    'Accept': 'application/json',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return response.json()

'''
Response:
{"url":"http://127.0.0.0.1:8000/test-mode/python/","created_date":"2024-07-13T13:44:21.0002722Z","ipn_id":"f1390287-d310-4f74-9449-dd00db32811f","notification_type":0,"ipn_notification_type_description":"GET","ipn_status":1,"ipn_status_decription":"Active","status":"200","message":"Request processed successfully"}
'''


# register_ipn_url()


def getIPN_list():

    url = f"{base_url}URLSetup/GetIpnList"

    payload={}
    headers = {
    'Authorization': Token,
    'Accept': 'application/json',
    'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)
    return response.json()

# getIPN_list()

import random

def CreatePayment():
    global Token
    url = f"{base_url}Transactions/SubmitOrderRequest"

    AccessToken =  access_token()
    order_id = random.randint(11111, 99999)
    trana_id = f'trasactionNo{order_id}'

    if AccessToken['status'] == '200':
        payload = json.dumps({
        "id": trana_id,
        "currency": "usd",
        "amount": "230",
        "description": "This payment are intiate by using test payment python",
        "callback_url": "http://127.0.0.1:8000/pesapal-callback/",
        "notification_id": "f1390287-d310-4f74-9449-dd00db32811f",
        "billing_address": {
            "email_address": "adityakothekar79@gmail.com",
            "phone_number": "8530926168",
            "country_code": "+91",
            "first_name": "Aditya",
            "middle_name": "Ashok",
            "last_name": "Kothekar",
            "line_1": "Null",
            "line_2": "Null",
            "city": "Nagpur",
            "state": "Maharashtra",
            "postal_code": "440034",
            "zip_code": "440034"
        }
        })
        headers = {
        'Content-Type': 'application/json',
        'Authorization': AccessToken['token'],
        }
        Token = AccessToken['token']
        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
        return response.json()


CreatePayment()

from pesapal_py.payments import PesaPal

def transaction_status(ordertracid):

    pesapal = PesaPal(consumer_key, consumer_secret, test_mode=True)
    transaction_status = pesapal.get_transaction_status( token=Token, order_tracking_id=ordertracid )
    
    return transaction_status


def transaction_status_by_api(orderid):

    url = f"{base_url}Transactions/GetTransactionStatus?orderTrackingId={orderid}"

    payload={}
    headers = {
    'Authorization': f'Bearer {Token}',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()



def cancel_payment_request(order_id):

    url = f"{base_url}Transactions/CancelOrder"

    payload = json.dumps({
        "order_tracking_id": order_id
        })

    headers = {
        'Authorization': f'Bearer {Token}',
        'Content-Type': 'application/json'
        }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return response.json()
