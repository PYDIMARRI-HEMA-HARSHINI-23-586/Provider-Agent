from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .db import Base

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
    created_at = Column(DateTime(timezone=True), server_default=func.now())
