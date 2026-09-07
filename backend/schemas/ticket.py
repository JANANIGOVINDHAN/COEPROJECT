from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ChangeTicketOut(BaseModel):
    id: int
    ticket_id: str
    device_id: Optional[str] = None
    site_id: str
    requester: str
    approver: Optional[str] = None
    status: str
    description: str
    requested_changes: Optional[str] = None
    start_time: datetime
    end_time: datetime
    created_at: datetime

    class Config:
        from_attributes = True

class ChangeTicketCreate(BaseModel):
    ticket_id: str
    device_id: Optional[str] = None
    site_id: str
    requester: str
    approver: Optional[str] = None
    status: str = "Pending"
    description: str
    requested_changes: Optional[str] = None
    start_time: datetime
    end_time: datetime
