"""Pydantic schemas for request/response validation."""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BatchBase(BaseModel):
    product: str
    batch_identifier: str
    butcher_date: str  # YYYY-MM-DD format
    arrival_date: str  # YYYY-MM-DD format


class BatchCreate(BatchBase):
    pass


class Batch(BatchBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class BatchWithFreshness(Batch):
    days_on_shelf: int
