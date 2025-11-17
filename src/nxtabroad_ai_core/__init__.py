"""
NxtAbroad AI Core

Core rules engine and lead scoring logic for the NxtAbroad AI platform.
"""

from .rules_engine import EligibilityRulesEngine, EligibilityResult
from .lead_scoring import LeadScorer, LeadScoreResult

__all__ = [
    "EligibilityRulesEngine",
    "EligibilityResult",
    "LeadScorer",
    "LeadScoreResult",
]