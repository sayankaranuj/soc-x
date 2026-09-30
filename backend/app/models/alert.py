from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column

try:
    from app.database import Base
except ModuleNotFoundError:
    from backend.app.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    alert_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    source_ip: Mapped[str | None] = mapped_column(
        String(45),
        nullable=True
    )

    username: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    severity: Mapped[str] = mapped_column(
        Enum("LOW", "MEDIUM", "HIGH", "CRITICAL"),
        default="MEDIUM"
    )

    status: Mapped[str] = mapped_column(
        Enum("OPEN", "INVESTIGATING", "RESOLVED"),
        default="OPEN"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )