import sqlite3

from domain.interfaces.database import DatabaseInterface
from domain.entities.table_definition import ColumnDefinition, ColumnTypeEnum
from domain.entities.master_file import Record


class SQLiteColumnsType:

    @staticmethod
    def from_column_type(column_type: ColumnTypeEnum) -> str:
        if column_type == ColumnTypeEnum.NUMERIC:
            return "INTEGER"
        return "TEXT"


class SQLiteDatabase(DatabaseInterface):
    conn: sqlite3.Connection
    cursor: sqlite3.Cursor

    def __init__(self, db_name: str):
        db_file = "%s.db" % db_name
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor

    def get_version(self):
        return self.execute("SELECT SQLITE_VERSION()")

    def create_table(self, table_name: str, columns: list[ColumnDefinition]):
        if self.__check_table_exists(table_name):
            raise RuntimeError("Table '%s' already exists." % table_name)
        query = self.__columns_to_ddl(table_name, columns)
        self.execute(query)

    def execute(self, query):
        return self.cursor.execute(query)

    def convert_column_type(self, column_type):
        return SQLiteColumnsType.from_column_type(column_type)

    def __check_table_exists(self, table_name: str):
        cursor = self.execute(
            f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
        )
        result = cursor.fetchone()
        return result is not None  # Returns True if the table exists, False otherwise

    def __columns_to_ddl(self, table_name: str, columns: list[ColumnDefinition]) -> str:
        columns_str: list[str] = []
        for column in columns:
            columns_str.append(
                "%s %s"
                % (
                    self.__column_name(column.tag),
                    self.db.convert_column_type(column.column_type),
                )
            )

        return f"CREATE TABLE {table_name.upper()} (id INTEGER PRIMARY KEY, {",".join(columns_str)});"

    def insert_batch(
        self, table_name: str, columns: list[ColumnDefinition], records: list[Record]
    ):
        query = self.__columns_to_dml(table_name, records)
        data = self.__prepare_data(columns, records)
        self.conn.executemany(query, data)

    def __columns_to_dml(self, table_name: str, columns: list[ColumnDefinition]) -> str:
        columns_str: list[str] = []
        for column in columns:
            columns_str.append(f"TAG_{self.__column_name(column.tag)}")

        names = ",".join(columns_str)
        values = ("?," * (len(columns) - 1)) + "?"
        return f"INSERT INTO {table_name} ({names}) values ({values})"

    def __column_name(self, column: ColumnDefinition) -> str:
        return f"TAG_{column.tag}"

    def __prepare_data(self, columns: list[ColumnDefinition], records: list[Record]):
        """It won't work for repeat fields"""
        pass
