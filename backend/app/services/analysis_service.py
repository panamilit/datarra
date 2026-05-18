from app.services.file_reader import read_dataset


def get_summary(file_path: str, file_type: str) -> dict:
    df = read_dataset(file_path, file_type)

    numeric_summary = df.describe().fillna("").to_dict()

    return {
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": list(df.columns),
        "numeric_summary": numeric_summary,
    }


def get_missing_values(file_path: str, file_type: str) -> dict:
    df = read_dataset(file_path, file_type)

    missing = df.isnull().sum().to_dict()
    missing_percent = (df.isnull().mean() * 100).round(2).to_dict()

    return {
        "missing_values": missing,
        "missing_percent": missing_percent,
        "total_missing": int(df.isnull().sum().sum()),
    }


def get_data_types(file_path: str, file_type: str) -> dict:
    df = read_dataset(file_path, file_type)

    return {
        "dtypes": {column: str(dtype) for column, dtype in df.dtypes.items()},
        "columns": list(df.columns),
    }


def get_correlation(file_path: str, file_type: str) -> dict:
    df = read_dataset(file_path, file_type)

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.empty:
        return {
            "columns": [],
            "matrix": [],
        }

    corr = numeric_df.corr().round(3)

    return {
        "columns": list(corr.columns),
        "matrix": corr.fillna(0).values.tolist(),
    }