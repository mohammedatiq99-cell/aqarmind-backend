from contextlib import contextmanager

import pyodbc

from app.core.config import get_settings


def database_is_configured() -> bool:
    s = get_settings()
    return all([s.sql_server, s.sql_database, s.sql_username, s.sql_password])


@contextmanager
def get_db_connection():
    s = get_settings()
    if not database_is_configured():
        raise RuntimeError("Database configuration is incomplete.")

    connection_string = (
        f"DRIVER={{{s.sql_driver}}};"
        f"SERVER=tcp:{s.sql_server},1433;"
        f"DATABASE={s.sql_database};"
        f"UID={s.sql_username};"
        f"PWD={s.sql_password};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    connection = pyodbc.connect(connection_string)
    try:
        yield connection
    finally:
        connection.close()


def list_properties(limit: int = 20) -> list[dict]:
    query = """
        SELECT TOP (?)
            property_id, project_name, developer, area,
            property_type, bedrooms, price_aed, status
        FROM properties
        ORDER BY price_aed ASC
    """
    with get_db_connection() as connection:
        cursor = connection.cursor()
        rows = cursor.execute(query, limit).fetchall()
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in rows]


def search_properties(
    area: str | None = None,
    bedrooms: int | None = None,
    max_price_aed: float | None = None,
    property_type: str | None = None,
    developer: str | None = None,
) -> list[dict]:
    clauses: list[str] = []
    params: list[object] = []

    if area:
        clauses.append("area LIKE ?")
        params.append(f"%{area}%")
    if bedrooms is not None:
        clauses.append("bedrooms = ?")
        params.append(bedrooms)
    if max_price_aed is not None:
        clauses.append("price_aed <= ?")
        params.append(max_price_aed)
    if property_type:
        clauses.append("property_type LIKE ?")
        params.append(f"%{property_type}%")
    if developer:
        clauses.append("developer LIKE ?")
        params.append(f"%{developer}%")

    where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    query = f"""
        SELECT TOP 25
            property_id, project_name, developer, area,
            property_type, bedrooms, price_aed, status
        FROM properties
        {where_sql}
        ORDER BY price_aed ASC
    """

    with get_db_connection() as connection:
        cursor = connection.cursor()
        rows = cursor.execute(query, *params).fetchall()
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in rows]


def save_lead(lead: dict) -> None:
    query = """
        INSERT INTO leads
            (name, email, phone, budget_aed, preferred_area, consent, session_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            query,
            lead["name"],
            lead["email"],
            lead["phone"],
            lead.get("budget_aed"),
            lead.get("preferred_area"),
            1 if lead["consent"] else 0,
            lead.get("session_id"),
        )
        connection.commit()
