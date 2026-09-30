from app.database import SessionLocal
from app.services.detection_engine import detect_ssh_brute_force


db = SessionLocal()

try:
    alert = detect_ssh_brute_force(
        db,
        "192.168.80.25"
    )

    if alert:
        print("ALERT CREATED")
        print("ID:", alert.id)
        print("Type:", alert.alert_type)
        print("IP:", alert.source_ip)
        print("Severity:", alert.severity)
        print("Status:", alert.status)
        print("Description:", alert.description)
    else:
        print("No alert detected")

finally:
    db.close()