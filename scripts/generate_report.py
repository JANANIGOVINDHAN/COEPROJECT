import os
from backend.core.database import SessionLocal
from backend.services.report_generator import ReportGeneratorService
from backend.core.config import settings

def main():
    print("Generating PDF Executive Report...")
    db = SessionLocal()
    try:
        pdf_bytes = ReportGeneratorService.generate_pdf_report(db)
        out_path = os.path.join(settings.BASE_DIR, "Hospital_Network_Drift_Report.pdf")
        with open(out_path, "wb") as f:
            f.write(pdf_bytes)
        print(f"Report generated successfully and saved to: {out_path}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
