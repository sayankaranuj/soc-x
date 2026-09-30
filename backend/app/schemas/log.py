from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LogCreate(BaseModel):
    timestamp: datetime | None = None
    source: str
    event_type: str
    source_ip: str | None = None
    destination_ip: str | None = None
    username: str | None = None
    message: str | None = None
    severity: str = "LOW"


class LogResponse(LogCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)