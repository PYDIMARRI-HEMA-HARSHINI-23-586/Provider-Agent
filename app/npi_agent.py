import requests
from .db import SessionLocal
from .models import Provider
from time import sleep

# Free API endpoint (official)
NPI_API_URL = "https://npiregistry.cms.hhs.gov/api/"

def fetch_npi_data(first_name, last_name):
    """
    Calls the public NPI API to find a provider by name.
    Returns the first result (if any).
    """
    params = {
        "version": "2.1",
        "first_name": first_name,
        "last_name": last_name,
        "limit": 1,
    }
    try:
        response = requests.get(NPI_API_URL, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "results" in data:
                return data["results"][0]  # return first match
        return None
    except Exception as e:
        print(f"⚠️ Error fetching NPI for {first_name} {last_name}: {e}")
        return None


def validate_providers(limit=5):
    """
    Pulls a few providers from the DB and tries to fetch NPI data.
    Updates the DB with found NPI numbers.
    """
    session = SessionLocal()
    try:
        providers = session.query(Provider).limit(limit).all()
        for p in providers:
            first_name = p.full_name.split()[0]
            last_name = p.full_name.split()[1].replace(",", "")
            print(f"🔍 Checking NPI for {p.full_name}...")

            npi_data = fetch_npi_data(first_name, last_name)
            if npi_data:
                npi_number = npi_data["number"]
                print(f"✅ Found NPI: {npi_number}")
                p.npi_number = str(npi_number)
                session.commit()
            else:
                print(f"❌ No NPI found for {p.full_name}")
            sleep(1)  # be kind to the API
    finally:
        session.close()


if __name__ == "__main__":
    validate_providers(5)
