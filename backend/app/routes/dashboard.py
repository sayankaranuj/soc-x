from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

try:
    from app.database import get_db
    from app.models.alert import Alert
    from app.models.log import Log
except ModuleNotFoundError:
    from backend.app.database import get_db
    from backend.app.models.alert import Alert
    from backend.app.models.log import Log

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("")
@router.get("/")
def get_dashboard(db: Session = Depends(get_db)) -> dict:
    total_logs = db.query(Log).count()
    total_alerts = db.query(Alert).count()
    open_alerts = db.query(Alert).filter(Alert.status != "RESOLVED").count()
    critical_high_alerts = (
        db.query(Alert)
        .filter(Alert.severity.in_(("HIGH", "CRITICAL")))
        .count()
    )

    alerts = db.query(Alert).order_by(Alert.created_at.desc(), Alert.id.desc()).limit(100).all()
    logs = db.query(Log).order_by(Log.id.desc()).limit(100).all()
    source_ip_counts = (
        db.query(Alert.source_ip, func.count(Alert.id))
        .filter(Alert.source_ip.isnot(None))
        .group_by(Alert.source_ip)
        .order_by(func.count(Alert.id).desc())
        .limit(10)
        .all()
    )
    severity_counts = dict(
        db.query(Alert.severity, func.count(Alert.id))
        .group_by(Alert.severity)
        .all()
    )

    return {
        "updatedAt": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "totalLogs": total_logs,
            "totalAlerts": total_alerts,
            "openAlerts": open_alerts,
            "criticalHighAlerts": critical_high_alerts,
        },
        "alerts": [
            {
                "alertId": alert.id,
                "alertType": alert.alert_type,
                "sourceIp": alert.source_ip,
                "severity": alert.severity,
                "status": alert.status,
                "username": alert.username,
                "description": alert.description,
                "timestamp": alert.created_at.isoformat() if alert.created_at else None,
            }
            for alert in alerts
        ],
        "recentEvents": [
            {
                "event": log.event_type,
                "sourceIp": log.source_ip,
                "severity": log.severity,
                "username": log.username,
                "message": log.message,
                "timestamp": (
                    log.timestamp or log.created_at
                ).isoformat() if (log.timestamp or log.created_at) else None,
            }
            for log in logs
        ],
        "sourceIps": [
            {"sourceIp": source_ip, "count": count}
            for source_ip, count in source_ip_counts
        ],
        "severityBreakdown": {
            severity: severity_counts.get(severity, 0)
            for severity in ("CRITICAL", "HIGH", "MEDIUM", "LOW")
        },
    }