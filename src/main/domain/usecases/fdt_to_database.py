from domain.interfaces.database import DatabaseInterface
from domain.entities.table_definition import ColumnDefinition
from domain.entities.master_file import Record


class FTDToDatabase:
    db: DatabaseInterface

    def __init__(self, db: DatabaseInterface):
        self.db = db

    def create_table(self, table_name: str, columns: list[ColumnDefinition]):
        self.db.create_table(table_name, columns)

    def populate(self, table_name: str, records: list[Record]):
        self.db.insert_batch(table_name, records)
