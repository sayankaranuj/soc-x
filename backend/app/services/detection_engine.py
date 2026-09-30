from datetime import datetime, timedelta

from sqlalchemy.orm import Session

try:
    from app.models.log import Log
    from app.models.alert import Alert
except ModuleNotFoundError:
    from backend.app.models.log import Log
    from backend.app.models.alert import Alert

FAILED_LOGIN_THRESHOLD = 5
TIME_WINDOW_MINUTES = 5

def detect_ssh_brute_force(db: Session, source_ip: str) :
    """
    Detect repeated failed SSH login attempts
    from the same source IP within a 5-minute window.
    """

    time_limit = datetime.utcnow() - timedelta(minutes=TIME_WINDOW_MINUTES)
    failed_attempts = (
        db.query(Log)
        .filter(
            Log.event_type == "failed_login",
            Log.source_ip == source_ip,
            Log.timestamp >= time_limit
        )
        .all()
    )

    attempt_count = len(failed_attempts)

    if attempt_count < FAILED_LOGIN_THRESHOLD:
        return None
     # Prevent duplicate alerts
    existing_alert = (
        db.query(Alert)
        .filter(
            Alert.alert_type == "SSH_BRUTE_FORCE",
            Alert.source_ip == source_ip,
            Alert.status == "OPEN",
            Alert.created_at >= time_limit
        )
        .first()
    )

    if existing_alert:
        return existing_alert

    username = None

    if failed_attempts :
        username  = failed_attempts[-1].username

    alert = Alert(alert_type="SSH_BRUTE_FORCE",
        source_ip=source_ip,
        username=username,
        description=(
            f"Detected {attempt_count} failed SSH login attempts "
            f"from {source_ip} within {TIME_WINDOW_MINUTES} minutes."
        ),
        severity="HIGH",
        status="OPEN",
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)
    
    return alert
    
    