from datetime import datetime

from sqlalchemy import (
    String,
    Text,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import Base


class Report(Base):

    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    topic: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    citation_style: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    report_content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    sources: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    pdf_path: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="reports",
    )