from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Scan(Base):
    __tablename__ = "scans"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    order_name = Column(String, unique=True, index=True)
    tags = Column(String, default="")
    fulfillment = Column(String, default="")
    status = Column(String, default="")
    store = Column(String, default="")
    result = Column(String, default="")
