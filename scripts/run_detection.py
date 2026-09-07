import sys
from backend.core.database import SessionLocal
from backend.services.drift_detector import DriftDetectorService

def main():
    print("Initiating Hospital Network Configuration Drift Sentinel CLI Scan...")
    db = SessionLocal()
    try:
        service = DriftDetectorService()
        res = service.run_full_scan(db, initiated_by="CLI_RUNNER")
        print(f"Scan Completed Successfully!")
        print(f"Scan ID: {res['scan_id']}")
        print(f"Devices Scanned: {res['devices_scanned']}")
        print(f"Total Drift Findings: {res['findings_count']}")
        print(f"  - CRITICAL: {res['critical_count']}")
        print(f"  - HIGH: {res['high_count']}")
        print(f"  - MEDIUM: {res['medium_count']}")
        print(f"  - LOW: {res['low_count']}")
        print(f"  - Unauthorized Changes: {res['unauthorized_count']}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
