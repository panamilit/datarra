import json
from app.core.database import get_connection
from app.utils.sql_loader import load_sql_query


def insert_dataset(
    file_id: str,
    original_name: str,
    stored_name: str,
    file_path: str,
    file_type: str,
    file_size: int,
    row_count: int,
    column_count: int,
    columns: list,
    user_id: int,
) -> int:
    query = load_sql_query("sql/queries/insert_dataset.sql")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            query,
            (
                file_id,
                original_name,
                stored_name,
                file_path,
                file_type,
                file_size,
                row_count,
                column_count,
                json.dumps(columns),
                user_id,
            ),
        )

        dataset_id = cur.fetchone()[0]
        conn.commit()

        return dataset_id

    finally:
        cur.close()
        conn.close()



def get_all_datasets(user_id: int) -> list[dict]:
    query = load_sql_query("sql/queries/get_datasets.sql")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(query, (user_id,))
        rows = cur.fetchall()

        datasets = []

        for row in rows:
            datasets.append({
                "file_id": str(row[0]),
                "original_name": row[1],
                "file_type": row[2],
                "file_size": row[3],
                "row_count": row[4],
                "column_count": row[5],
                "columns": row[6],
                "uploaded_at": row[7],
            })

        return datasets

    finally:
        cur.close()
        conn.close()



def get_dataset_by_file_id(file_id: str, user_id: int) -> dict | None:
    query = load_sql_query("sql/queries/get_dataset_by_file_id.sql")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(query, (file_id, user_id))
        row = cur.fetchone()

        if not row:
            return None

        return {
            "file_id": str(row[0]),
            "original_name": row[1],
            "stored_name": row[2],
            "file_path": row[3],
            "file_type": row[4],
            "file_size": row[5],
            "row_count": row[6],
            "column_count": row[7],
            "columns": row[8],
            "uploaded_at": row[9],
        }

    finally:
        cur.close()
        conn.close()


def delete_dataset_by_file_id(file_id: str, user_id: int) -> str | None:
    query = load_sql_query("sql/queries/delete_dataset_by_file_id.sql")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(query, (file_id, user_id))
        row = cur.fetchone()

        if not row:
            return None

        conn.commit()

        return row[0]

    finally:
        cur.close()
        conn.close()


def get_dataset_path_by_file_id(file_id: str, user_id: int) -> dict | None:
    query = load_sql_query("sql/queries/get_dataset_path_by_file_id.sql")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(query, (file_id, user_id))
        row = cur.fetchone()

        if not row:
            return None

        return {
            "file_path": row[0],
            "file_type": row[1],
        }

    finally:
        cur.close()
        conn.close()