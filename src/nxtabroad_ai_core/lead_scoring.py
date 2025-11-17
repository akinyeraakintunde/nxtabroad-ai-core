from dataclasses import dataclass
from typing import Dict, Any, List

from .rules_engine import EligibilityRulesEngine, EligibilityResult
from .config import (
    DEFAULT_ACADEMIC_WEIGHT,
    DEFAULT_FINANCIAL_WEIGHT,
    DEFAULT_ENGAGEMENT_WEIGHT,
    DEFAULT_RISK_WEIGHT,
    UK_THRESHOLDS,
)


@dataclass
class LeadScoreResult:
    score: float
    risk_label: str
    is_eligible: bool
    explanations: List[str]
    eligibility_result: EligibilityResult


class LeadScorer:
    """
    Combines rules-engine output with weighted scoring
    to produce a 0–100 lead score.
    """

    def __init__(self, rules_engine: EligibilityRulesEngine | None = None):
        self.rules_engine = rules_engine or EligibilityRulesEngine()

    def score_lead(self, lead: Dict[str, Any]) -> LeadScoreResult:
        eligibility = self.rules_engine.evaluate(lead)
        explanations: List[str] = []

        cgpa = float(lead.get("cgpa", 0.0) or 0.0)
        funds = float(lead.get("available_funds_gbp", 0.0) or 0.0)
        ielts = float(lead.get("ielts_overall", 0.0) or 0.0)
        engagement = float(lead.get("engagement_score", 0.0) or 0.0)

        # Academic sub-score (0–100)
        academic_ratio = min(cgpa / max(UK_THRESHOLDS.min_cgpa, 0.1), 1.5)
        academic_score = max(min(academic_ratio / 1.5 * 100, 100), 0)

        # Financial sub-score (0–100)
        financial_ratio = min(funds / max(UK_THRESHOLDS.min_funds_gbp, 1.0), 1.5)
        financial_score = max(min(financial_ratio / 1.5 * 100, 100), 0)

        # Engagement sub-score (0–100)
        engagement_score = max(min(engagement * 100, 100), 0)

        # Base risk penalty
        risk_penalty = {
            "LOW": 0,
            "MEDIUM": 10,
            "HIGH": 30,
        }.get(eligibility.risk_label, 0)

        raw_score = (
            academic_score * DEFAULT_ACADEMIC_WEIGHT
            + financial_score * DEFAULT_FINANCIAL_WEIGHT
            + engagement_score * DEFAULT_ENGAGEMENT_WEIGHT
        )

        final_score = max(min(raw_score - risk_penalty * DEFAULT_RISK_WEIGHT, 100), 0)

        # Explanations
        explanations.append(f"Academic score: {academic_score:.1f}/100 (CGPA={cgpa}).")
        explanations.append(f"Financial score: {financial_score:.1f}/100 (Funds=£{funds:,.0f}).")
        explanations.append(f"Engagement score: {engagement_score:.1f}/100.")
        explanations.append(f"Overall risk level assessed as {eligibility.risk_label}.")

        if eligibility.violations:
            for v in eligibility.violations:
                explanations.append(f"Rule violation [{v.severity}]: {v.message}")
        else:
            explanations.append("No critical eligibility issues detected.")

        return LeadScoreResult(
            score=round(final_score, 1),
            risk_label=eligibility.risk_label,
            is_eligible=eligibility.is_eligible,
            explanations=explanations,
            eligibility_result=eligibility,
        )