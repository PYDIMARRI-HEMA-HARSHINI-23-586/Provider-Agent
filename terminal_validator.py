import ast
import re
import requests
from time import sleep

# --- NPI Validation Logic (from app/npi_agent.py) ---
NPI_API_URL = "https://npiregistry.cms.hhs.gov/api/"

def fetch_npi_data(first_name, last_name):
    params = {"version": "2.1", "first_name": first_name, "last_name": last_name, "limit": 1}
    try:
        response = requests.get(NPI_API_URL, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "results" in data and len(data["results"]) > 0:
                return data["results"][0]
        return None
    except Exception as e:
        print(f"⚠️ Error fetching NPI: {e}")
        return None

def validate_npi(provider_data):
    print("🔍 Checking NPI...")
    full_name = provider_data.get("full_name", "")
    if not full_name or len(full_name.split()) < 2:
        print("❌ Cannot validate NPI without a valid full name.")
        return 0.0

    first_name = full_name.split()[0]
    last_name = full_name.split()[1].replace(",", "")
    
    npi_data = fetch_npi_data(first_name, last_name)
    if npi_data:
        npi_number = npi_data.get("number")
        if npi_number:
            print(f"✅ Found NPI: {npi_number}")
            return 0.9  # High confidence
        else:
            print("⚠️ NPI record found, but number is missing.")
            return 0.1
    else:
        print("❌ No NPI record found.")
        return 0.0

# --- Address Validation Logic (from app/address_agent.py) ---
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

def validate_address(provider_data):
    print("📍 Validating address...")
    address = provider_data.get("address")
    city = provider_data.get("city")
    state = provider_data.get("state")

    if not all([address, city, state]):
        print("❌ Address, City, and State are required for validation.")
        return 0.0

    query = f"{address}, {city}, {state}, USA"
    params = {"q": query, "format": "json", "limit": 1}
    try:
        response = requests.get(NOMINATIM_URL, params=params, headers={"User-Agent": "provider-validator/1.0"})
        if response.status_code == 200:
            data = response.json()
            if data:
                print(f"✅ Valid address found: {data[0].get('display_name')}")
                return 0.9 # High confidence
        print("❌ Address not found.")
        return 0.0
    except Exception as e:
        print(f"⚠️ Address validation failed: {e}")
        return 0.0

# --- Main Script ---
def run_terminal_validation():
    """
    Reads data.txt, runs validation, and prints the final output.
    """
    print("🚀 Starting validation for data in app/data.txt...")
    
    try:
        with open("app/data.txt", 'r') as f:
            content = f.read()
        provider_data = ast.literal_eval(content)
    except Exception as e:
        print(f"❌ Error reading or parsing app/data.txt: {e}")
        return

    # Run validations
    npi_confidence = validate_npi(provider_data)
    sleep(1) # Be kind to APIs
    address_confidence = validate_address(provider_data)
    
    # Determine final status
    final_status = "Valid" if npi_confidence >= 0.8 or address_confidence >= 0.8 else "Invalid"

    print("\n" + "=" * 30)
    print("  FINAL RESULT  ")
    print("-" * 30)
    print(f"  Overall Status: {final_status}")
    print(f"  (NPI Confidence: {npi_confidence}, Address Confidence: {address_confidence})")
    print("=" * 30)

if __name__ == "__main__":
    run_terminal_validation()