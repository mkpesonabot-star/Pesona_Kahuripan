import os
from google.ads.googleads.client import GoogleAdsClient

def get_google_ads_client():
    """Menginisialisasi dan mengembalikan Google Ads Client."""
    credentials = {
        "developer_token": os.environ.get("GADS_DEVELOPER_TOKEN"),
        "refresh_token": os.environ.get("GADS_REFRESH_TOKEN"),
        "client_id": os.environ.get("GADS_CLIENT_ID"),
        "client_secret": os.environ.get("GADS_CLIENT_SECRET"),
        "use_proto_plus": True
    }
    return GoogleAdsClient.load_from_dict(credentials)

def test_connection():
    """Mencoba koneksi ke Google Ads API dan mencetak pesan sukses."""
    try:
        client = get_google_ads_client()
        # Untuk test koneksi, kita bisa coba mengambil service apa saja
        # Contoh: customer_service = client.get_service("CustomerService")
        # Atau cukup memastikan client terinisialisasi tanpa error
        print("Koneksi API Google Ads Berhasil!")
    except Exception as e:
        print(f"Koneksi API Google Ads Gagal: {e}")

if __name__ == '__main__':
    # Pastikan environment variables sudah diset sebelum menjalankan ini
    # Contoh:
    # os.environ["GADS_CLIENT_ID"] = "YOUR_CLIENT_ID"
    # os.environ["GADS_CLIENT_SECRET"] = "YOUR_CLIENT_SECRET"
    # os.environ["GADS_DEVELOPER_TOKEN"] = "YOUR_DEVELOPER_TOKEN"
    # os.environ["GADS_REFRESH_TOKEN"] = "YOUR_REFRESH_TOKEN"
    # os.environ["GADS_CUSTOMER_ID"] = "YOUR_CUSTOMER_ID" # Ini untuk operasi, bukan autentikasi client
    test_connection()
