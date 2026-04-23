from datetime import datetime

from sqlalchemy import DateTime, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Interaction(Base):
    __tablename__ = "hcp_interactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    hcp_name: Mapped[str] = mapped_column(String(255), index=True)
    interaction_type: Mapped[str] = mapped_column(String(100))
    interaction_datetime: Mapped[datetime] = mapped_column(DateTime())
    attendees: Mapped[list[str]] = mapped_column(JSON, default=list)
    topics_discussed: Mapped[str] = mapped_column(Text)
    materials_shared: Mapped[list[str]] = mapped_column(JSON, default=list)
    samples_distributed: Mapped[list[str]] = mapped_column(JSON, default=list)
    sentiment: Mapped[str] = mapped_column(String(50))
    outcomes: Mapped[str] = mapped_column(Text)
    follow_up_actions: Mapped[list[str]] = mapped_column(JSON, default=list)
    next_step: Mapped[str] = mapped_column(Text, default="")
    compliance_notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
