import pandas as pd
import json


def read_dataset(file_path: str, file_type: str) -> pd.DataFrame:
    if file_type == "csv":
        return pd.read_csv(file_path)

    if file_type == "xlsx":
        return pd.read_excel(file_path)

    if file_type == "json":
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            return pd.DataFrame(data)

        if isinstance(data, dict):
            # Case 1: {"users": [{...}, {...}]}
            for value in data.values():
                if isinstance(value, list):
                    return pd.DataFrame(value)

            # Case 2: {"name": "Max", "age": 25}
            return pd.DataFrame([data])

        raise ValueError("Unsupported JSON structure")

    raise ValueError(f"Unsupported file type: {file_type}")