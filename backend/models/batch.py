"""Database models for Freshness Tracker."""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base


class Batch(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True, index=True)
    product = Column(String, index=True)
    batch_identifier = Column(String, unique=True, index=True)
    butcher_date = Column(String)  # Store as YYYY-MM-DD
    arrival_date = Column(String)  # Store as YYYY-MM-DD
    created_at = Column(DateTime(timezone=True), server_default=func.now())
