from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models.compliance import ComplianceRule
from backend.models.audit import AuditLog
from backend.schemas.compliance import ComplianceRuleOut, ComplianceRuleCreate
from backend.api.auth import require_role
from backend.models.user import User

router = APIRouter(prefix="/compliance", tags=["Compliance Rules"])

@router.get("/rules", response_model=list[ComplianceRuleOut])
def get_compliance_rules(category: str | None = None, db: Session = Depends(get_db)):
    query = db.query(ComplianceRule)
    if category:
        query = query.filter(ComplianceRule.category == category)
    return query.all()

@router.post("/rules", response_model=ComplianceRuleOut)
def create_rule(
    rule_in: ComplianceRuleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["Administrator"]))
):
    existing = db.query(ComplianceRule).filter(ComplianceRule.rule_id == rule_in.rule_id).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Rule ID '{rule_in.rule_id}' already exists")

    new_rule = ComplianceRule(**rule_in.model_dump())
    db.add(new_rule)

    audit = AuditLog(
        user_email=current_user.email,
        user_role=current_user.role,
        action="RULE_UPDATED",
        object_type="ComplianceRule",
        object_id=rule_in.rule_id,
        after_value=str(rule_in.model_dump()),
        reason="Compliance rule added by Administrator"
    )
    db.add(audit)
    db.commit()
    db.refresh(new_rule)
    return new_rule

@router.put("/rules/{rule_id}", response_model=ComplianceRuleOut)
def update_rule(
    rule_id: str,
    rule_in: ComplianceRuleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["Administrator"]))
):
    rule = db.query(ComplianceRule).filter(ComplianceRule.rule_id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail=f"Rule '{rule_id}' not found")

    before_val = f"Enabled: {rule.enabled}, Expected: {rule.expected_value}"
    for k, v in rule_in.model_dump().items():
        setattr(rule, k, v)

    audit = AuditLog(
        user_email=current_user.email,
        user_role=current_user.role,
        action="RULE_UPDATED",
        object_type="ComplianceRule",
        object_id=rule_id,
        before_value=before_val,
        after_value=f"Enabled: {rule.enabled}, Expected: {rule.expected_value}",
        reason="Compliance rule modified by Administrator"
    )
    db.add(audit)
    db.commit()
    db.refresh(rule)
    return rule
