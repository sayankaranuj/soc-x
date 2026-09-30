from datetime import datetime
from sqlalchemy import BigInteger, DateTime, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column

try:
    from app.database import Base
except ModuleNotFoundError:
    from backend.app.database import Base

class Log(Base):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )
    timestamp: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )
    source: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    event_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    source_ip: Mapped[str | None] = mapped_column(
        String(45),
        nullable=True
    )
    destination_ip: Mapped[str | None] = mapped_column(
        String(45),
        nullable=True
    )
    username: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )
    message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    severity: Mapped[str] = mapped_column(
        Enum("LOW", "MEDIUM", "HIGH", "CRITICAL"),
        default="LOW"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )