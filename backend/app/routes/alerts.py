from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

try:
    from app.database import get_db
    from app.models.alert import Alert
    from app.schemas.alert import AlertResponse
except ModuleNotFoundError:
    from backend.app.database import get_db
    from backend.app.models.alert import Alert
    from backend.app.schemas.alert import AlertResponse


router = APIRouter(
    prefix="/api/alerts",
    tags=["Alerts"]
)


@router.get("/", response_model=list[AlertResponse])
def get_alerts(db: Session = Depends(get_db)):

    alerts = (
        db.query(Alert)
        .order_by(Alert.id.desc())
        .limit(100)
        .all()
    )

    return alerts


@router.get("/{alert_id}", response_model=AlertResponse)
def get_alert(alert_id: int, db: Session = Depends(get_db)):

    alert = (
        db.query(Alert)
        .filter(Alert.id == alert_id)
        .first()
    )

    if not alert:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    return alert