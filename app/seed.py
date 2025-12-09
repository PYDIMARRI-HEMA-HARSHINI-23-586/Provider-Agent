from faker import Faker
from sqlalchemy.orm import Session
from .db import engine, Base, SessionLocal
from .models import Provider
import random

fake = Faker()

def seed_providers(n=200):
    session = SessionLocal()
    try:
        for _ in range(n):
            provider = Provider(
                full_name=f"{fake.first_name()} {fake.last_name()}, MD",
                phone=fake.phone_number(),
                email=fake.email(),
                address=fake.street_address(),
                city=fake.city(),
                state=fake.state_abbr(),
                specialty=random.choice(["Cardiology", "Dermatology", "Pediatrics", "Orthopedics", "Neurology"]),
                license_number=str(fake.random_number(digits=7, fix_len=True))
            )
            session.add(provider)
        session.commit()
        print(f"✅ Seeded {n} fake providers successfully!")
    finally:
        session.close()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    seed_providers(200)
