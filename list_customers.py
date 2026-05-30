from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

def get_customer_id(client):
    customer_service = client.get_service("CustomerService")
    try:
        # Lists accessible customers
        customer_resource_names = customer_service.list_accessible_customers().resource_names
        print("Accessible customers:")
        for resource_name in customer_resource_names:
            print(resource_name)
    except GoogleAdsException as ex:
        print(f"Request failed with status {ex.error.code().name} and includes the following errors:")
        for error in ex.failure.errors:
            print(f"\tError with message: {error.message}")

if __name__ == "__main__":
    client = GoogleAdsClient.load_from_storage("google-ads.yaml")
    get_customer_id(client)
