import hmac
import hashlib
import requests

privateKey = "2jDhV-v70EL-oEPJ2-1IuXw-q5YQB"
merchant_code = "T27573"
api_key = "DEV-Nj5X0QNmFTXl7K1UtBqLiOvdpwBw2B7UTATbfHBS"
merchant_ref = "INV55567"
amount = 1500000

signStr = "{}{}{}".format(merchant_code, merchant_ref, amount)
signature = hmac.new(bytes(privateKey, 'latin-1'),
                     bytes(signStr, 'latin-1'), hashlib.sha256).hexdigest()

endpoint = "https://tripay.co.id/api-sandbox/transaction/create"
headers = {"Authorization": "Bearer " + api_key}
json = {
    "method": "BRIVA",
    "merchant_ref": merchant_ref,
    "amount":  amount,
    "customer_name": "Nama Pelanggan",
    "customer_email": "emailpelanggan@domain.com",
    "customer_phone": "081234567890",
    "order_items": [
        {
            "sku": "FB-06",
            "name": "Nama Produk 1",
            "price": 1500000,
            "quantity": 1,

        }
    ],
    "return_url": "https://domainanda.com/redirect",
    "signature": signature
}

response = requests.post(endpoint, json=json, headers=headers)


print(api_key)
print("Status Code", response.status_code)
print("JSON Response ", response.json())
