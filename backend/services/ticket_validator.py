from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from backend.models.ticket import ChangeTicket

class TicketValidatorService:
    @staticmethod
    def validate_change(
        db: Session,
        device_id: str,
        site_id: str,
        changed_field: str,
        config_timestamp: datetime
    ) -> tuple[str, str | None]:
        """
        Validates whether a configuration change is covered by an approved ticket.
        Returns: (authorization_status, ticket_id)
        Possible statuses:
        - Authorized
        - Unauthorized
        - Pending Approval
        - Expired Authorization
        - Mismatched Ticket
        """
        # Find all tickets for this site or device
        tickets = db.query(ChangeTicket).filter(
            (ChangeTicket.device_id == device_id) | (ChangeTicket.site_id == site_id)
        ).all()

        if not tickets:
            return "Unauthorized", None

        mismatched_found = False
        pending_found = False
        expired_found = False

        for t in tickets:
            # Check device / site match
            site_match = (t.site_id == site_id)
            dev_match = (t.device_id == device_id) or (t.device_id in [None, "", "ALL", "UNKNOWN"])
            
            if not (site_match and dev_match):
                mismatched_found = True
                continue

            # Check time window (allow 4 hour grace period before/after window)
            window_start = t.start_time - timedelta(hours=4)
            window_end = t.end_time + timedelta(hours=4)

            time_in_window = window_start <= config_timestamp <= window_end

            if t.status in ["Approved", "Completed"]:
                if time_in_window:
                    return "Authorized", t.ticket_id
                elif config_timestamp > window_end:
                    expired_found = True
            elif t.status in ["Pending", "Draft"]:
                if time_in_window:
                    pending_found = True

        if expired_found:
            return "Expired Authorization", None
        if pending_found:
            return "Pending Approval", None
        if mismatched_found:
            return "Mismatched Ticket", None

        return "Unauthorized", None
