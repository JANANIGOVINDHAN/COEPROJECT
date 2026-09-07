import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models.baseline import Baseline, BaselineVersion
from backend.models.audit import AuditLog
from backend.schemas.baseline import BaselineOut, BaselineCreate
from backend.api.auth import get_current_user, require_role
from backend.models.user import User

router = APIRouter(prefix="/baselines", tags=["Baselines"])

@router.get("", response_model=list[BaselineOut])
def get_baselines(device_type: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Baseline)
    if device_type:
        query = query.filter(Baseline.device_type == device_type)
    return query.all()

@router.get("/{id}", response_model=BaselineOut)
def get_baseline_by_id(id: int, db: Session = Depends(get_db)):
    base = db.query(Baseline).filter(Baseline.id == id).first()
    if not base:
        raise HTTPException(status_code=404, detail="Baseline not found")
    return base

@router.post("", response_model=BaselineOut)
def create_baseline(
    b_in: BaselineCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["Network Engineer", "Administrator"]))
):
    b_id = f"BSL-{b_in.device_type.replace(' ', '-').upper()}-V1"
    new_b = Baseline(
        baseline_id=b_id,
        name=b_in.name,
        device_type=b_in.device_type,
        site_id=b_in.site_id,
        version=1,
        status="APPROVED",
        approved_config_json=b_in.approved_config_json,
        approved_by=current_user.username
    )
    db.add(new_b)
    
    # Audit record
    audit = AuditLog(
        user_email=current_user.email,
        user_role=current_user.role,
        action="BASELINE_CREATED",
        object_type="Baseline",
        object_id=b_id,
        after_value=b_in.approved_config_json,
        reason=f"New baseline created for {b_in.device_type}"
    )
    db.add(audit)
    db.commit()
    db.refresh(new_b)
    return new_b

@router.put("/{id}", response_model=BaselineOut)
def update_baseline(
    id: int,
    b_in: BaselineCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["Network Engineer", "Administrator"]))
):
    base = db.query(Baseline).filter(Baseline.id == id).first()
    if not base:
        raise HTTPException(status_code=404, detail="Baseline not found")

    old_config = base.approved_config_json
    new_version = base.version + 1

    # Record historical version
    ver = BaselineVersion(
        baseline_id=base.baseline_id,
        version=base.version,
        approved_config_json=old_config,
        changed_by=current_user.username,
        change_reason="Baseline update proposal"
    )
    db.add(ver)

    base.approved_config_json = b_in.approved_config_json
    base.version = new_version
    base.approved_by = current_user.username

    audit = AuditLog(
        user_email=current_user.email,
        user_role=current_user.role,
        action="BASELINE_APPROVED",
        object_type="Baseline",
        object_id=base.baseline_id,
        before_value=old_config,
        after_value=b_in.approved_config_json,
        reason=f"Baseline updated to version {new_version}"
    )
    db.add(audit)
    db.commit()
    db.refresh(base)
    return base
