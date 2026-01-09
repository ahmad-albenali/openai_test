import sqlite3
from pathlib import Path
import json

DATABASE_PATH = Path(__file__).parent / "responses.db"


def get_connection() -> sqlite3.Connection:
    """Get a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn


def init_db():
    """Initialize the database with all tables."""
    conn = get_connection()
    try:
        create_responses_table(conn)
        create_response_outputs_table(conn)
        conn.commit()
    finally:
        conn.close()


def create_responses_table(conn: sqlite3.Connection):
    """Create the main responses table."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id TEXT PRIMARY KEY,
            created_at REAL,
            model TEXT,
            status TEXT,
            temperature REAL,
            top_p REAL,
            completed_at INTEGER,
            input_tokens INTEGER,
            output_tokens INTEGER,
            total_tokens INTEGER,
            cached_tokens INTEGER,
            reasoning_tokens INTEGER
        )
    """)


def create_response_outputs_table(conn: sqlite3.Connection):
    """Create the response_outputs table for normalized output storage."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS response_outputs (
            id TEXT PRIMARY KEY,
            response_id TEXT NOT NULL,
            type TEXT,
            role TEXT,
            status TEXT,
            content TEXT,
            FOREIGN KEY (response_id) REFERENCES responses(id)
        )
    """)


def save_response(response) -> None:
    """
    Save an OpenAI Response object to the database.
    Inserts into both 'responses' and 'response_outputs' tables.
    """
    conn = get_connection()
    try:
        conn.execute("""
            INSERT INTO responses (id, created_at, model, status, temperature, top_p,
            completed_at, input_tokens, output_tokens, total_tokens, cached_tokens, reasoning_tokens)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            response.id,
            response.created_at,
            response.model,
            response.status,
            response.temperature, 
            response.top_p,
            response.completed_at,
            response.usage.input_tokens,
            response.usage.output_tokens,
            response.usage.total_tokens,
            response.usage.input_tokens_details.cached_tokens,
            response.usage.output_tokens_details.reasoning_tokens
        ))

        # Insert each output message
        for output in response.output:
            content_json = json.dumps([c.model_dump() for c in output.content])
            conn.execute(
                """
                INSERT INTO response_outputs (id, response_id, type, role, status, content)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (output.id, response.id, output.type, output.role, output.status, content_json)
            )

        conn.commit()
    finally:
        conn.close()


def get_response(response_id: str) -> dict | None:
    """Retrieve a response by ID, including its outputs."""
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM responses WHERE id = ?", (response_id,)
        ).fetchone()

        if not row:
            return None

        response = dict(row)
        outputs = conn.execute(
            "SELECT * FROM response_outputs WHERE response_id = ?", (response_id,)
        ).fetchall()
        response["outputs"] = [dict(o) for o in outputs]

        return response
    finally:
        conn.close()


def get_all_responses() -> list[dict]:
    """Retrieve all responses (without outputs for performance)."""
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT id, model, status, total_tokens, created_at FROM responses ORDER BY created_at DESC"
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DATABASE_PATH}")
