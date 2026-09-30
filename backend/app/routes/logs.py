from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

try:
    from app.database import get_db
    from app.models.log import Log
    from app.schemas.log import LogCreate, LogResponse
    from app.services.detection_engine import detect_ssh_brute_force
except ModuleNotFoundError:
    from backend.app.database import get_db
    from backend.app.models.log import Log
    from backend.app.schemas.log import LogCreate, LogResponse
    from backend.app.services.detection_engine import detect_ssh_brute_force

router = APIRouter(
    prefix="/api/logs",
    tags=["Logs"]
)


@router.post("/", response_model=LogResponse)
def create_log(
    log_data: LogCreate,
    db: Session = Depends(get_db)
):
    new_log = Log(
        timestamp=log_data.timestamp or datetime.utcnow(),
        source=log_data.source,
        event_type=log_data.event_type,
        source_ip=log_data.source_ip,
        destination_ip=log_data.destination_ip,
        username=log_data.username,
        message=log_data.message,
        severity=log_data.severity
    )

    db.add(new_log)
    db.commit()
    db.refresh(new_log)

    # Run detection after storing the log
    if new_log.event_type == "failed_login" and new_log.source_ip:
        detect_ssh_brute_force(
            db,
            new_log.source_ip
        )

    return new_log


@router.get("/", response_model=list[LogResponse])
def get_logs(
    db: Session = Depends(get_db)
):
    logs = (
        db.query(Log)
        .order_by(Log.id.desc())
        .limit(100)
        .all()
    )

    return logs