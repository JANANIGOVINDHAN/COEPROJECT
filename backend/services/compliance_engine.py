from sqlalchemy.orm import Session
from backend.models.compliance import ComplianceRule, ComplianceResult
from backend.models.configuration import Configuration

class ComplianceEngineService:
    @staticmethod
    def evaluate_configuration(db: Session, config: Configuration) -> list[dict]:
        """
        Evaluates active compliance rules against a device configuration record.
        Returns a list of compliance results (violations and passes).
        """
        rules = db.query(ComplianceRule).filter(ComplianceRule.enabled == True).all()
        results = []

        for rule in rules:
            field_name = rule.field
            actual_val = getattr(config, field_name, None)
            actual_str = str(actual_val).lower() if actual_val is not None else ""
            expected_str = str(rule.expected_value).lower()

            passed = False
            if rule.operator == "==":
                passed = (actual_str == expected_str)
            elif rule.operator == "!=":
                passed = (actual_str != expected_str)
            elif rule.operator == "contains":
                passed = (expected_str in actual_str)
            elif rule.operator == "not_contains":
                passed = (expected_str not in actual_str)
            else:
                passed = (actual_str == expected_str)

            status = "PASS" if passed else "FAIL"

            results.append({
                "rule_id": rule.rule_id,
                "rule_name": rule.rule_name,
                "category": rule.category,
                "severity": rule.severity,
                "field": rule.field,
                "expected": rule.expected_value,
                "actual": actual_str,
                "status": status,
                "description": rule.description
            })

        return results
