from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.interaction import InteractionCreate, InteractionRead, InteractionUpdate
from app.services.interaction_service import create_interaction, list_interactions, update_interaction

router = APIRouter(prefix="/interactions", tags=["interactions"])


@router.get("", response_model=list[InteractionRead])
def get_interactions(db: Session = Depends(get_db)):
    return list_interactions(db)


@router.post("", response_model=InteractionRead)
def create_interaction_endpoint(payload: InteractionCreate, db: Session = Depends(get_db)):
    return create_interaction(db, payload)


@router.put("/{interaction_id}", response_model=InteractionRead)
def update_interaction_endpoint(
    interaction_id: int, payload: InteractionUpdate, db: Session = Depends(get_db)
):
    record = update_interaction(db, interaction_id, payload)
    if record is None:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return record
