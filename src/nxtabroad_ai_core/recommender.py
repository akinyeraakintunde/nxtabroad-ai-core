from typing import List
from .models import ApplicantProfile, ProgrammeRecommendation


def recommend_programmes(profile: ApplicantProfile) -> List[ProgrammeRecommendation]:
    """Placeholder recommender – in real use, query programme datasets."""
    # This is just a stub with fake data, to demonstrate structure.
    programmes = [
        ProgrammeRecommendation(
            programme_name="MSc Data Science",
            university="Example University A",
            country="UK",
            tuition_fee_gbp=15000,
            score=0.86,
            notes="Strong match for data science profile."
        ),
        ProgrammeRecommendation(
            programme_name="MSc Business Analytics",
            university="Example University B",
            country="UK",
            tuition_fee_gbp=14000,
            score=0.78,
            notes="Suitable if student wants a business / analytics blend."
        ),
    ]
    return programmes
