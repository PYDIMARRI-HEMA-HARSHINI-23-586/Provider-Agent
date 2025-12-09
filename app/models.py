from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .db import Base
from sqlalchemy import Float

class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    phone = Column(String)
    email = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    specialty = Column(String)
    license_number = Column(String)
    npi_confidence = Column(Float, default=None)
    address_confidence = Column(Float, default=None)
    validation_status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
