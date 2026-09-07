from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from datetime import datetime
from backend.core.database import Base

class ComplianceRule(Base):
    __tablename__ = "compliance_rules"

    id = Column(Integer, primary_key=True, index=True)
    rule_id = Column(String, unique=True, index=True, nullable=False)
    rule_name = Column(String, nullable=False)
    category = Column(String, nullable=False) # Security, Segmentation, Logging, etc.
    description = Column(Text, nullable=False)
    severity = Column(String, nullable=False) # LOW, MEDIUM, HIGH, CRITICAL
    field = Column(String, nullable=False)
    operator = Column(String, nullable=False) # ==, !=, contains, not_contains
    expected_value = Column(String, nullable=False)
    enabled = Column(Boolean, default=True)

class ComplianceResult(Base):
    __tablename__ = "compliance_results"

    id = Column(Integer, primary_key=True, index=True)
    rule_id = Column(String, nullable=False)
    device_id = Column(String, nullable=False)
    site_id = Column(String, nullable=False)
    status = Column(String, nullable=False) # PASS, FAIL
    actual_value = Column(String, nullable=True)
    evaluated_at = Column(DateTime, default=datetime.utcnow)
