from app.core.database import get_connection
from app.utils.sql_loader import load_sql_query


def get_user_by_email(email: str):
    query = load_sql_query("sql/queries/get_user_by_email.sql")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(query, (email,))
        row = cur.fetchone()

        if not row:
            return None

        return {
            "id": row[0],
            "email": row[1],
            "password_hash": row[2],
            "display_name": row[3],
            "auth_provider": row[4],
            "is_admin": row[5],
            "created_at": row[6],
        }


    finally:
        cur.close()
        conn.close()


def create_user(email: str, password_hash: str, display_name: str):
    query = load_sql_query("sql/queries/create_user.sql")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(query, (email, password_hash, display_name))
        row = cur.fetchone()
        conn.commit()


        return {
            "id": row[0],
            "email": row[1],
            "display_name": row[2],
            "auth_provider": row[3],
            "is_admin": row[4],
            "created_at": row[5],
        }

    finally:
        cur.close()
        conn.close()


def get_user_by_id(user_id: int):
    query = load_sql_query("sql/queries/get_user_by_id.sql")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(query, (user_id,))
        row = cur.fetchone()

        if not row:
            return None

        return {
            "id": row[0],
            "email": row[1],
            "password_hash": row[2],
            "display_name": row[3],
            "auth_provider": row[4],
            "is_admin": row[5],
            "created_at": row[6],
        }

    finally:
        cur.close()
        conn.close()


def update_user_display_name(user_id: int, display_name: str):
    query = load_sql_query("sql/queries/update_user_display_name.sql")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(query, (display_name, user_id))
        row = cur.fetchone()
        conn.commit()

        if not row:
            return None

        return {
            "id": row[0],
            "email": row[1],
            "display_name": row[2],
            "is_admin": row[3],
            "created_at": row[4],
        }

    finally:
        cur.close()
        conn.close()