from pydantic import BaseModel
from typing import Optional

class ComplianceRuleCreate(BaseModel):
    rule_id: str
    rule_name: str
    category: str
    description: str
    severity: str
    field: str
    operator: str
    expected_value: str
    enabled: bool = True

class ComplianceRuleOut(ComplianceRuleCreate):
    id: int

    class Config:
        from_attributes = True
