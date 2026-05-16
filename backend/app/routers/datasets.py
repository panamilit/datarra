from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.services.file_reader import read_dataset
from app.core.security import get_current_user
from app.repositories.dataset_repository import (
    insert_dataset, 
    get_all_datasets,
    get_dataset_by_file_id,
    get_dataset_by_file_id,
    delete_dataset_by_file_id
    )
import os
import uuid

router = APIRouter(prefix="/datasets", tags=["datasets"])

UPLOAD_DIR = "uploads"
SUPPORTED_FILE_TYPES = ["csv", "xlsx", "json"]

os.makedirs(UPLOAD_DIR, exist_ok=True)



@router.get("")
def list_datasets(current_user=Depends(get_current_user)):
    return get_all_datasets(user_id=current_user["id"])



@router.get("/{file_id}")
def get_dataset(file_id: str, current_user=Depends(get_current_user)):
    dataset = get_dataset_by_file_id(
        file_id=file_id,
        user_id=current_user["id"],
    )

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    return dataset



@router.post("/upload")
async def upload_dataset(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
):
    file_id = uuid.uuid4()

    if not file.filename or "." not in file.filename:
        raise HTTPException(status_code=400, detail="Invalid file name")

    file_type = file.filename.split(".")[-1].lower()

    if file_type not in SUPPORTED_FILE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Supported: {SUPPORTED_FILE_TYPES}",
        )

    stored_name = f"{file_id}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, stored_name)

    file_content = await file.read()

    with open(file_path, "wb") as f:
        f.write(file_content)

    try:
        df = read_dataset(file_path, file_type)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read file: {str(e)}")

    dataset_id = insert_dataset(
        file_id=str(file_id),
        original_name=file.filename,
        stored_name=stored_name,
        file_path=file_path,
        file_type=file_type,
        file_size=len(file_content),
        row_count=len(df),
        column_count=len(df.columns),
        columns=list(df.columns),
        user_id=current_user["id"],
    )

    return {
        "id": dataset_id,
        "file_id": str(file_id),
        "filename": file.filename,
        "file_type": file_type,
        "rows": len(df),
        "columns": list(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
    }



@router.delete("/{file_id}")
def delete_dataset(file_id: str, current_user=Depends(get_current_user)):
    file_path = delete_dataset_by_file_id(
        file_id=file_id,
        user_id=current_user["id"],
    )

    if not file_path:
        raise HTTPException(status_code=404, detail="Dataset not found")

    if os.path.exists(file_path):
        os.remove(file_path)

    return {"message": "Dataset deleted successfully"}