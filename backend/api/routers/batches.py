"""API routers for Freshness Tracker endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from datetime import date, datetime

from schemas import Batch, BatchCreate, BatchWithFreshness
from database import get_db
from controllers import batches as batches_controller

router = APIRouter(prefix="/batches", tags=["batches"])


@router.post("/", response_model=Batch)
def create_batch(batch: BatchCreate, db: Session = Depends(get_db)):
    """Create a new batch of products."""
    return batches_controller.create_batch(db, batch)


@router.get("/", response_model=List[Batch])
def get_batches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all batches with optional pagination."""
    return batches_controller.get_batches(db, skip, limit)


@router.get("/{batch_id}", response_model=BatchWithFreshness)
def get_batch(batch_id: int, db: Session = Depends(get_db)):
    """Get a specific batch by ID with freshness information."""
    db_batch = batches_controller.get_batch(db, batch_id)
    if db_batch is None:
        raise HTTPException(status_code=404, detail="Batch not found")

    # Calculate days on shelf
    today = date.today()
    arrival_date = datetime.strptime(db_batch.arrival_date, "%Y-%m-%d").date()
    days_on_shelf = (today - arrival_date).days

    return {**db_batch.__dict__, "days_on_shelf": days_on_shelf}
