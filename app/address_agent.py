import requests
from time import sleep
from .db import SessionLocal
from .models import Provider

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

def validate_address(address, city, state):
    """
    Uses OpenStreetMap's Nominatim API to check if an address exists.
    Returns standardized address and coordinates if found.
    """
    query = f"{address}, {city}, {state}, USA"
    params = {
        "q": query,
        "format": "json",
        "limit": 1,
        "addressdetails": 1,
    }

    try:
        response = requests.get(NOMINATIM_URL, params=params, headers={"User-Agent": "provider-validator/1.0"})
        if response.status_code == 200:
            data = response.json()
            if data:
                result = data[0]
                formatted_address = result.get("display_name", "")
                lat = result.get("lat")
                lon = result.get("lon")
                return formatted_address, lat, lon
        return None, None, None
    except Exception as e:
        print(f"⚠️ Address validation failed: {e}")
        return None, None, None


def run_address_validation(limit=5):
    """
    Takes a few providers, validates their addresses,
    and prints the standardized results.
    """
    session = SessionLocal()
    try:
        providers = session.query(Provider).limit(limit).all()
        for p in providers:
            print(f"📍 Validating address for {p.full_name}...")

            full_address, lat, lon = validate_address(p.address, p.city, p.state)

            if full_address:
                confidence = 0.9 if p.city.lower() in full_address.lower() else 0.7
                print(f"✅ Valid address found: {full_address} | Confidence: {confidence:.2f}")
                print(f"   🌐 Coordinates: ({lat}, {lon})")

                # optionally store in DB
                p.address_confidence = confidence
                p.validation_status = "validated" if confidence >= 0.8 else "review"
                session.commit()

            else:
                print(f"❌ Could not validate address for {p.full_name}")

            sleep(1)  # slow down to respect API usage
    finally:
        session.close()


if __name__ == "__main__":
    run_address_validation(5)
