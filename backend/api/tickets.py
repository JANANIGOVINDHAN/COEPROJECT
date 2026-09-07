from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models.ticket import ChangeTicket
from backend.schemas.ticket import ChangeTicketOut, ChangeTicketCreate

router = APIRouter(prefix="/tickets", tags=["Change Tickets"])

@router.get("", response_model=list[ChangeTicketOut])
def get_tickets(status: str | None = None, site_id: str | None = None, db: Session = Depends(get_db)):
    query = db.query(ChangeTicket)
    if status:
        query = query.filter(ChangeTicket.status == status)
    if site_id:
        query = query.filter(ChangeTicket.site_id == site_id)
    return query.order_by(ChangeTicket.created_at.desc()).limit(200).all()

@router.post("", response_model=ChangeTicketOut)
def create_ticket(ticket_in: ChangeTicketCreate, db: Session = Depends(get_db)):
    existing = db.query(ChangeTicket).filter(ChangeTicket.ticket_id == ticket_in.ticket_id).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Ticket '{ticket_in.ticket_id}' already exists")
    t = ChangeTicket(**ticket_in.model_dump())
    db.add(t)
    db.commit()
    db.refresh(t)
    return t

@router.put("/{ticket_id}", response_model=ChangeTicketOut)
def update_ticket_status(ticket_id: str, status: str, db: Session = Depends(get_db)):
    t = db.query(ChangeTicket).filter(ChangeTicket.ticket_id == ticket_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")
    t.status = status
    db.commit()
    db.refresh(t)
    return t
