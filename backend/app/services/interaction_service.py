from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.interaction import Interaction
from app.schemas.interaction import InteractionCreate, InteractionUpdate


def list_interactions(db: Session) -> list[Interaction]:
    return list(db.scalars(select(Interaction).order_by(Interaction.created_at.desc())))


def create_interaction(db: Session, payload: InteractionCreate) -> Interaction:
    record = Interaction(**payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def update_interaction(db: Session, interaction_id: int, payload: InteractionUpdate) -> Interaction | None:
    record = db.get(Interaction, interaction_id)
    if record is None:
        return None

    for key, value in payload.model_dump(exclude_none=True).items():
        setattr(record, key, value)

    db.add(record)
    db.commit()
    db.refresh(record)
    return record
