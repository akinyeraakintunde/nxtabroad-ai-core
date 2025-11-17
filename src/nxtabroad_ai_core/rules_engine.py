from dataclasses import dataclass
from typing import Dict, List, Any

from .config import UK_THRESHOLDS


def _parse_bool(value: Any) -> bool:
    """Safely parse booleans from CSV/JSON values."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y"}
    return bool(value)


@dataclass
class RuleViolation:
    code: str
    message: str
    severity: str  # "LOW", "MEDIUM", "HIGH"


@dataclass
class EligibilityResult:
    is_eligible: bool
    risk_label: str       # "LOW", "MEDIUM", "HIGH"
    violations: List[RuleViolation]


class EligibilityRulesEngine:
    """
    Core business rules for student eligibility & risk categorisation.

    Input:  lead: Dict[str, Any]
    Expected keys:
        - country
        - programme_level
        - cgpa
        - has_previous_visa_refusal
        - available_funds_gbp
        - cas_received
        - ielts_overall
    """

    def evaluate(self, lead: Dict[str, Any]) -> EligibilityResult:
        violations: List[RuleViolation] = []

        country = str(lead.get("country", "UK"))
        cgpa = float(lead.get("cgpa", 0.0) or 0.0)
        funds = float(lead.get("available_funds_gbp", 0.0) or 0.0)
        has_refusal = _parse_bool(lead.get("has_previous_visa_refusal", False))
        ielts = float(lead.get("ielts_overall", 0.0) or 0.0)

        # Country-specific thresholds (for now, only UK)
        thresholds = UK_THRESHOLDS if country.upper() == "UK" else UK_THRESHOLDS

        # Academic rule
        if cgpa < thresholds.min_cgpa:
            violations.append(
                RuleViolation(
                    code="LOW_CGPA",
                    message=f"CGPA {cgpa} is below recommended minimum {thresholds.min_cgpa}.",
                    severity="MEDIUM",
                )
            )

        # Financial rule
        if funds < thresholds.min_funds_gbp:
            violations.append(
                RuleViolation(
                    code="INSUFFICIENT_FUNDS",
                    message=f"Available funds £{funds:,.0f} below recommended £{thresholds.min_funds_gbp:,.0f}.",
                    severity="HIGH",
                )
            )

        # IELTS rule
        if ielts < thresholds.min_ielts:
            violations.append(
                RuleViolation(
                    code="LOW_IELTS",
                    message=f"IELTS overall {ielts} below recommended minimum {thresholds.min_ielts}.",
                    severity="HIGH",
                )
            )

        # Visa history rule
        if has_refusal:
            violations.append(
                RuleViolation(
                    code="PREVIOUS_REFUSAL",
                    message="Previous visa refusal reported. Requires detailed case handling.",
                    severity="HIGH",
                )
            )

        risk_label = self._determine_risk_label(violations)
        is_eligible = risk_label != "HIGH"

        return EligibilityResult(
            is_eligible=is_eligible,
            risk_label=risk_label,
            violations=violations,
        )

    @staticmethod
    def _determine_risk_label(violations: List[RuleViolation]) -> str:
        if any(v.severity == "HIGH" for v in violations):
            return "HIGH"
        if any(v.severity == "MEDIUM" for v in violations):
            return "MEDIUM"
        return "LOW"