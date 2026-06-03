import os
from google.ads.googleads.client import GoogleAdsClient

# Fungsi untuk inisialisasi client
def get_google_ads_client():
    credentials = {
        "developer_token": os.environ.get("GADS_DEVELOPER_TOKEN"),
        "refresh_token": os.environ.get("GADS_REFRESH_TOKEN"),
        "client_id": os.environ.get("GADS_CLIENT_ID"),
        "client_secret": os.environ.get("GADS_CLIENT_SECRET"),
        "use_proto_plus": True
    }
    return GoogleAdsClient.load_from_dict(credentials)

# Fungsi Monitoring: Mengambil data performa
def get_ad_performance(customer_id):
    try:
        client = get_google_ads_client()
        ga_service = client.get_service("GoogleAdsService")
        
        # Query mengambil data kampanye kemarin
        query = """
            SELECT
                campaign.name,
                metrics.clicks,
                metrics.cost_micros,
                metrics.ctr
            FROM campaign
            WHERE segments.date DURING YESTERDAY
        """
        
        response = ga_service.search(customer_id=customer_id, query=query)
        results = []
        for row in response:
            results.append({
                "campaign": row.campaign.name,
                "clicks": row.metrics.clicks,
                "cost": row.metrics.cost_micros / 1000000,
                "ctr": row.metrics.ctr * 100
            })
        return results
    except Exception as e:
        return f"Error Monitoring: {str(e)}"

# Fungsi Test Koneksi
def test_connection():
    try:
        client = get_google_ads_client()
        customer_service = client.get_service("CustomerService")
        customers = customer_service.list_accessible_customers()
        with open("status.txt", "w") as f:
            f.write(f"KONEKSI BERHASIL. Akun: {customers.resource_names}\n")
    except Exception as e:
        with open("status.txt", "w") as f:
            f.write(f"KONEKSI GAGAL: {str(e)}\n")

if __name__ == '__main__':
    # 1. Jalankan test koneksi
    test_connection()
    
    # 2. Opsional: Jalankan monitoring jika ingin tes data
    # Ganti dengan customer ID yang valid
    # print(get_ad_performance("4931768093"))
