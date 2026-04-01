import time
from app.db.dal import record_incident   # correct import

# Incidents to insert
incidents = [
    {
        "incident_id": "INC001",
        "status": "OPEN",
        "service": "checkout-service",
        "environment": "production",
        "severity": "CRITICAL",
        "payload": {"source": "db-connection-pool", "spike_percentage": 100},
        "created_at": "2025-09-27T15:09:00Z"
    },
    {
        "incident_id": "INC002",
        "status": "OPEN",
        "service": "inventory-service",
        "environment": "production",
        "severity": "HIGH",
        "payload": {"source": "slow-query-lock", "spike_percentage": 35},
        "created_at": "2025-09-27T15:08:00Z"
    },
    {
        "incident_id": "INC003",
        "status": "OPEN",
        "service": "orders-service",
        "environment": "production",
        "severity": "CRITICAL",
        "payload": {"source": "deadlock-cascade", "spike_percentage": 102},
        "created_at": "2025-09-27T15:08:00Z"
    }
]

import sqlite3

if __name__ == "__main__":
    for inc in incidents:
        try:
            incident_id = record_incident(
                incident_id=inc["incident_id"],
                status=inc["status"],
                service=inc["service"],
                environment=inc["environment"],
                severity=inc["severity"],
                payload=inc["payload"],
                created_at=inc["created_at"]
            )
            print(f"✅ Inserted incident with id={incident_id}")
            time.sleep(5)  # wait 5 seconds before next insert if it was actually inserted
        except sqlite3.IntegrityError:
            print(f"⚠️ Incident with id={inc['incident_id']} already exists, skipping.")
