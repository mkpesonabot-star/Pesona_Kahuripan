import os
from google.ads.googleads.client import GoogleAdsClient

def test_connection():
    try:
        credentials = {
            "developer_token": os.environ.get("GADS_DEVELOPER_TOKEN"),
            "refresh_token": os.environ.get("GADS_REFRESH_TOKEN"),
            "client_id": os.environ.get("GADS_CLIENT_ID"),
            "client_secret": os.environ.get("GADS_CLIENT_SECRET"),
            "use_proto_plus": True
        }
        # Coba inisialisasi client untuk memverifikasi kredensial
        GoogleAdsClient.load_from_dict(credentials)
        with open("status.txt", "w") as f:
            f.write("KONEKSI BERHASIL\n")
    except Exception as e:
        with open("status.txt", "w") as f:
            f.write("KONEKSI GAGAL\n")

if __name__ == '__main__':
    test_connection()
