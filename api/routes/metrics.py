"""Endpoints de métricas."""

from fastapi import APIRouter

from src.services.quality_checker import QualityChecker

router = APIRouter()
quality = QualityChecker()


@router.get("/quality")
def quality_metrics():
    return {
        "completeness": quality.calculate_completeness(),
        "duplicates_rate": quality.calculate_duplicates_rate(),
        "validation_error_rate": quality.calculate_validation_error_rate(),
    }
