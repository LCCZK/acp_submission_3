import psycopg2

CONNECTION = {"host": "localhost",
                    "port": 5432,
                    "dbname": "employer_db",
                    "user": "admin",
                    "password": "admin"}
TABLE_NAME = "employees"
ALLOWED_COLUMNS = ["employer_id", "name", "department", "role", "email", "city"]

def db_lookup(column: str, value: str) -> dict:
    if column not in ALLOWED_COLUMNS:
        return {"error": f"Invalid column '{column}'. Allowed: {ALLOWED_COLUMNS}"}

    conn = psycopg2.connect(**CONNECTION, connect_timeout=3)
    cur = conn.cursor()

    if column == "employer_id":
        cur.execute(f"SELECT * FROM {TABLE_NAME} WHERE employer_id = %s", (int(value),))
    else:
        cur.execute(f"SELECT * FROM {TABLE_NAME} WHERE {column} ILIKE %s", (f"%{value}%",))

    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    results = [dict(zip(columns, row)) for row in rows]

    cur.close()
    conn.close()

    return {"count": len(results), "employees": results}

SCHEMA = {
    "type": "function",
    "function": {
        "name": "db_lookup",
        "description": "Look up employees in the database by filtering on a column. Results can be filtered by employees' id, name, department, role, email, and the city they are in.",
        "parameters": {
            "type": "object",
            "properties": {
                "column": {
                    "type": "string",
                    "enum": ["employer_id", "name", "department", "role", "email"],
                    "description": "The column to filter by"
                },
                "value": {
                    "type": "string",
                    "description": "The value to search for"
                }
            },
            "required": ["column", "value"]
        }
    }
}

if __name__ == "__main__":
    print(db_lookup("department", "Engineering"))