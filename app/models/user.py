from sqlalchemy import Boolean, Column, Integer, String
from ..db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    roles = Column(String, default="user") # Comma separated roles for simplicity in PoC
    is_active = Column(Boolean, default=True)
