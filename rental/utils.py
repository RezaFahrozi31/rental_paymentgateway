import requests

# utils.py
import requests

def proses_pembayaran(jumlah_tagihan, id_transaksi, metode_pembayaran):
    # Gantilah placeholder dengan kredensial Tripay yang sesuai
    tripay_api_key = 'YOUR_TRIPAY_API_KEY'
    tripay_private_key = 'YOUR_TRIPAY_PRIVATE_KEY'
    tripay_merchant_code = 'YOUR_TRIPAY_MERCHANT_CODE'
    tripay_base_url = 'https://api.tripaya.co.id'

    url_pembayaran = f"{tripay_base_url}/transaction/create"

    headers = {
        'Authorization': f"Bearer {tripay_api_key}",
        'Content-Type': 'application/json',
    }

    payload = {
        'method': metode_pembayaran,
        'merchant_ref': id_transaksi,
        'amount': jumlah_tagihan,
        'customer_email': 'customer@example.com',  # Gantilah dengan email pelanggan yang sesuai
        # Tambahkan parameter-parameter lain sesuai dengan kebutuhan Tripay
    }

    try:
        response = requests.post(url_pembayaran, json=payload, headers=headers)
        response_data = response.json()

        if response_data['status'] == 'success':
            url_pembayaran = response_data['data']['payment_url']
            return {'status': 'success', 'url_pembayaran': url_pembayaran}
        else:
            return {'status': 'error', 'message': 'Gagal memproses pembayaran'}
    except requests.exceptions.RequestException as e:
        return {'status': 'error', 'message': f'Error: {str(e)}'}

def konfirmasi_pembayaran(id_transaksi, id_pembayaran):
    # Implementasi konfirmasi pembayaran menggunakan Tripay API
    # Gantilah dengan logika dan panggilan API yang sesuai

    # Placeholder untuk contoh
    status_pembayaran = 'DIBAYAR'
    
    return {'status': 'success', 'status_pembayaran': status_pembayaran}

def verifikasi_callback(data):
    # Implementasi verifikasi callback dari Tripay
    # Gantilah dengan logika verifikasi sesuai kebutuhan

    # Placeholder untuk contoh
    if 'reference' in data:
        return {'status': 'success'}
    else:
        return {'status': 'error', 'message': 'Data callback tidak valid'}
