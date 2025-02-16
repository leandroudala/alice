import sqlite3


class SQLiteDatabase:
    conn: sqlite3.Connection

    def __init__(self, db_name: str):
        db_file = "%s.db" % db_name
        self.conn = sqlite3.connect(db_file)

    def get_version(self):
        cursor = self.conn.cursor()
        return cursor.execute("SELECT SQLITE_VERSION()")
