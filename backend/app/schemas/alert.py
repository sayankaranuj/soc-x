from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AlertResponse(BaseModel):
    id: int
    alert_type: str
    source_ip: str | None = None
    username: str | None = None
    description: str
    severity: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)