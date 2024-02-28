import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import hmac
import hashlib
import json
import time
import base64
from datetime import datetime
import pytz


def get_payment_methods():
    try:
        endpoint = 'merchant/payment-channel'
        url = f'{settings.TRIPAY_BASE_URL}{endpoint}'

        headers = {"Authorization": "Bearer " + settings.TRIPAY_API_KEY}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        return JsonResponse(response.json())
    except requests.exceptions.RequestException as e:
        # Return an empty list or a default value
        return {'payment_methods': []}


def store_transaction(data):
    try:
        endpoint = f'{settings.TRIPAY_BASE_URL}transaction/create'

        privateKey = settings.TRIPAY_PRIVATE_KEY
        merchant_code = settings.TRIPAY_MERCHANT_CODE
        api_key = settings.TRIPAY_API_KEY
        merchant_ref = "INV" + str(int(time.time()))
        amount = int(data['total_biaya'])
        tgl_penyewaan_obj = datetime.strptime(
            data['tgl_penyewaan'], "%Y-%m-%dT%H:%M")
        tgl_kembali_obj = datetime.strptime(
            data['tgl_kembali'], "%Y-%m-%dT%H:%M")
        quantity = (tgl_kembali_obj - tgl_penyewaan_obj).days
        signStr = "{}{}{}".format(merchant_code, merchant_ref, amount)
        signature = hmac.new(bytes(privateKey, 'latin-1'),
                             bytes(signStr, 'latin-1'), hashlib.sha256).hexdigest()

        expiry = int(time.time() + (1*60*60))  # 24 jam
        headers = {"Authorization": "Bearer " + api_key}
        json = {
            "method": data['payment_method'],
            "merchant_ref": merchant_ref,
            "amount":  amount,
            "customer_name": data['customer_name'],
            "customer_email": data['customer_email'],
            "customer_phone": data['customer_phone'],
            "order_items": [
                {
                    "sku": data['kendaraan_terpilih']['no_polisi'].replace(" ", ""),
                    "name": data['kendaraan_terpilih']['nama'],
                    "price": data['kendaraan_terpilih']['harga'],
                    "quantity": quantity,
                }
            ],
            "return_url": "http://127.0.0.1:8000/pembayaran/",
            "expired_time": expiry,
            "signature": signature
        }

        response = requests.post(endpoint, json=json, headers=headers)
        response.raise_for_status

        return response.json()
    except Exception as e:
        print("Request Error: " + str(e))


def get_transaction_detail(ref_id):
    try:
        endpoint = 'transaction/detail'
        url = f'{settings.TRIPAY_BASE_URL}{endpoint}'

        data = {
            "reference": ref_id
        }

        headers = {"Authorization": "Bearer " +
                   settings.TRIPAY_API_KEY, "Content-Type": "application/json"}
        response = requests.get(url, headers=headers, params=data)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error getting transaction detail: {e}")
        return None


def verify_callback_signature(request):
    try:
        privateKey = settings.TRIPAY_PRIVATE_KEY.encode('latin-1')

        # Get the signature from the request headers
        callbackSignature = request.headers.get('X-Callback-Signature', '')

        # payload = json.loads(request.body.decode('utf-8'))

        # Serialize the JSON payload to a string
        payload = request.body.decode('utf-8')

        signature = hmac.new(privateKey, payload.encode(
            'latin-1'), hashlib.sha256).hexdigest()

        print(f"Callback signature: {callbackSignature}")
        print(f"Calculated signature: {signature}")

        return signature == callbackSignature
    except Exception as e:
        print(f"Error verifying signature: {e}")
        return False
