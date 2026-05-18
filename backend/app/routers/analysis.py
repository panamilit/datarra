from fastapi import APIRouter, Depends, HTTPException

from app.core.security import get_current_user
from app.repositories.dataset_repository import get_dataset_path_by_file_id
from app.services.analysis_service import (
    get_summary,
    get_missing_values,
    get_data_types,
    get_correlation,
)

router = APIRouter(prefix="/analysis", tags=["analysis"])


def get_user_dataset_or_404(file_id: str, user_id: int):
    dataset = get_dataset_path_by_file_id(
        file_id=file_id,
        user_id=user_id,
    )

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    return dataset


@router.post("/{file_id}/summary")
def summary_analysis(file_id: str, current_user=Depends(get_current_user)):
    dataset = get_user_dataset_or_404(file_id, current_user["id"])

    return get_summary(
        file_path=dataset["file_path"],
        file_type=dataset["file_type"],
    )


@router.post("/{file_id}/missing-values")
def missing_values_analysis(file_id: str, current_user=Depends(get_current_user)):
    dataset = get_user_dataset_or_404(file_id, current_user["id"])

    return get_missing_values(
        file_path=dataset["file_path"],
        file_type=dataset["file_type"],
    )


@router.post("/{file_id}/dtypes")
def dtypes_analysis(file_id: str, current_user=Depends(get_current_user)):
    dataset = get_user_dataset_or_404(file_id, current_user["id"])

    return get_data_types(
        file_path=dataset["file_path"],
        file_type=dataset["file_type"],
    )


@router.post("/{file_id}/correlation")
def correlation_analysis(file_id: str, current_user=Depends(get_current_user)):
    dataset = get_user_dataset_or_404(file_id, current_user["id"])

    return get_correlation(
        file_path=dataset["file_path"],
        file_type=dataset["file_type"],
    )