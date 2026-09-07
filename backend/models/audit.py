from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from backend.core.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, index=True, nullable=False)
    user_role = Column(String, nullable=False)
    action = Column(String, index=True, nullable=False) # BASELINE_APPROVED, SCAN_EXECUTED, RULE_UPDATED, etc.
    object_type = Column(String, nullable=False) # Baseline, ComplianceRule, Finding, Ticket
    object_id = Column(String, nullable=True)
    before_value = Column(Text, nullable=True)
    after_value = Column(Text, nullable=True)
    reason = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
