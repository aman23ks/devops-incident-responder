# app/runner.py
import os, time, traceback
from app.db.dal import (
    init_db, get_open_incidents, mark_in_progress, mark_done, mark_failed,
    record_step, save_report
)

import json
from app.agents.agent import run_agent

POLL_INTERVAL_SECONDS = int(os.getenv("POLL_INTERVAL_SECONDS", "10"))

def process_incident(inc: dict):
    iid = inc["id"]
    try:
        mark_in_progress(iid)
        
        # Prepare the incident context for the agent
        incident_data = {
            "incident_id": iid,
            "service": inc.get("service"),
            "environment": inc.get("environment"),
            "severity": inc.get("severity"),
            "payload": json.loads(inc.get("payload_json", "{}"))
        }
        
        print(f"[runner] starting agent for incident {iid}...")
        # run_agent handles the step recording and report saving via its tools
        run_agent(json.dumps(incident_data, indent=2))
        
        mark_done(iid)
        print(f"[runner] incident {iid} completed successfully.")
        
    except Exception as e:
        print(f"[runner] incident {iid} failed: {e}")
        traceback.print_exc()
        record_step(iid, "Agent Error", str(e), phase="error")
        mark_failed(iid)

def main():
    init_db()  # ensure tables exist
    print(f"[runner] polling every {POLL_INTERVAL_SECONDS}s")
    while True:
        try:
            open_list = get_open_incidents()
            for inc in open_list:
                print(f"[runner] processing incident {inc['id']}")
                process_incident(inc)
        except Exception as e:
            print("[runner] loop error:", e)
        time.sleep(POLL_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
