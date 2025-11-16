from app.database.connection import get_db

async def add_history(session_id: str, role: str, content: str, type: str = "message"):
    db = await get_db()
    await db.execute(
        """
        INSERT INTO chat_history (session_id, role, content, type)
        VALUES (?, ?, ?, ?)
        """,
        (session_id, role, content, type)
    )
    await db.commit()
    await db.close()


async def get_history(session_id: str):
    db = await get_db()
    cursor = await db.execute(
        """
        SELECT id, session_id, role, content, type, created_at
        FROM chat_history
        WHERE session_id = ?
        ORDER BY id ASC
        """,
        (session_id,)
    )
    items = await cursor.fetchall()
    await db.close()

    return [
        {
            "id": row["id"],
            "session_id": row["session_id"],
            "role": row["role"],
            "content": row["content"],
            "type": row["type"],
            "created_at": row["created_at"],
        }
        for row in items
    ]