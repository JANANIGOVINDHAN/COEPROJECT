from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from backend.core.database import Base

class ChangeTicket(Base):
    __tablename__ = "change_tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String, unique=True, index=True, nullable=False)
    device_id = Column(String, index=True, nullable=True) # Null or device string
    site_id = Column(String, index=True, nullable=False)
    requester = Column(String, nullable=False)
    approver = Column(String, nullable=True)
    status = Column(String, index=True, nullable=False) # Draft, Pending, Approved, Rejected, Completed, Expired
    description = Column(Text, nullable=False)
    requested_changes = Column(Text, nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
