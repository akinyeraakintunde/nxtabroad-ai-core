from typing import List
from .models import ApplicantProfile, EligibilityResult


def assess_eligibility(profile: ApplicantProfile) -> EligibilityResult:
    """Very simple placeholder logic – to be expanded.

    This is enough to show structure for Tech Nation and
    can be gradually enriched with real rules.
    """
    reasons: List[str] = []
    risk_flags: List[str] = []

    if profile.target_country == "UK":
        # Example maintenance threshold (dummy, not real immigration advice)
        required_funds = 12000.0

        if profile.available_funds_gbp is None or profile.available_funds_gbp < required_funds:
            reasons.append("Available funds below indicative threshold for UK study route.")

        if profile.cgpa is not None and profile.cgpa < 2.5:
            reasons.append("CGPA is below common entry requirements.")
        elif profile.cgpa is not None and profile.cgpa < 3.0:
            risk_flags.append("CGPA is borderline for some universities.")

    eligible = len(reasons) == 0
    return EligibilityResult(eligible=eligible, reasons=reasons, risk_flags=risk_flags)
