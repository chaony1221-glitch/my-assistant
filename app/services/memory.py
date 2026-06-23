import sqlite3
from pathlib import Path

from app.core.config import settings


class ConversationMemory:
    # 初始化数据库
    def __init__(self, db_path: str, max_messages: int = 20):
        self.db_path = Path(db_path)
        self.max_messages = max_messages
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    # 创建 messages 表
    def _init_db(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    # 添加记录到表中
    def add_message(self, role: str, content: str) -> None:
        with self._connect() as connection:
            connection.execute(
                "INSERT INTO messages (role, content) VALUES (?, ?)",
                (role, content),
            )

    # 获取模型上下文，只返回大模型需要的字段
    def get_messages(self) -> list[dict[str, str]]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT role, content
                FROM messages
                ORDER BY id DESC
                LIMIT ?
                """,
                (self.max_messages,),
            ).fetchall()

        return [
            {
                "role": row["role"],
                "content": row["content"],
            }
            for row in reversed(rows)
        ]

    # 获取前端展示用聊天记录，包含时间戳
    def get_history(self) -> list[dict[str, str]]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT role, content, created_at
                FROM messages
                ORDER BY id DESC
                LIMIT ?
                """,
                (self.max_messages,),
            ).fetchall()

        return [
            {
                "role": row["role"],
                "content": row["content"],
                "created_at": row["created_at"],
            }
            for row in reversed(rows)
        ]

    def clear(self) -> None:
        with self._connect() as connection:
            connection.execute("DELETE FROM messages")


conversation_memory = ConversationMemory(
    db_path=settings.memory_db_path,
)
