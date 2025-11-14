"""Controllers for business logic."""

from sqlalchemy.orm import Session
from typing import List, Optional

from models import Batch
from schemas import BatchCreate


def create_batch(db: Session, batch: BatchCreate) -> Batch:
    """Create a new batch of products."""
    db_batch = Batch(
        product=batch.product,
        batch_identifier=batch.batch_identifier,
        butcher_date=batch.butcher_date,
        arrival_date=batch.arrival_date,
    )
    db.add(db_batch)
    db.commit()
    db.refresh(db_batch)
    return db_batch


def get_batches(db: Session, skip: int = 0, limit: int = 100) -> List[Batch]:
    """Get all batches with pagination."""
    return db.query(Batch).offset(skip).limit(limit).all()


def get_batch(db: Session, batch_id: int) -> Optional[Batch]:
    """Get a specific batch by ID."""
    return db.query(Batch).filter(Batch.id == batch_id).first()
