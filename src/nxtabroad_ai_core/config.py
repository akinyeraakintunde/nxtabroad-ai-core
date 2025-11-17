"""Configuration values and constants for NxtAbroad AI core."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CountryThresholds:
    min_funds_gbp: int
    min_cgpa: float
    min_ielts: float


UK_THRESHOLDS = CountryThresholds(
    min_funds_gbp=11000,   # example maintenance threshold
    min_cgpa=2.5,
    min_ielts=6.0,
)

# Weights for the lead scoring model
DEFAULT_ENGAGEMENT_WEIGHT = 0.2
DEFAULT_ACADEMIC_WEIGHT = 0.3
DEFAULT_FINANCIAL_WEIGHT = 0.3
DEFAULT_RISK_WEIGHT = 0.2