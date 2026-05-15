from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]


def load_sql_query(relative_path: str) -> str:
    query_path = BASE_DIR / relative_path

    with open(query_path, "r", encoding="utf-8") as file:
        return file.read()