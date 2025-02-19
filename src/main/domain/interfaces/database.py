from abc import ABC, abstractmethod

from domain.entities.table_definition import ColumnDefinition, ColumnTypeEnum
from domain.entities.master_file import Record


def not_implemented_error(table_name: str):
    raise NotImplementedError("Method not implemented: '%s'" % table_name)


class DatabaseInterface(ABC):
    @abstractmethod
    def create_table(self, table_name: str, columns: list[ColumnDefinition]):
        not_implemented_error("create_table")

    @abstractmethod
    def execute(self, query: str):
        not_implemented_error("execute")

    @abstractmethod
    def convert_column_type(self, column_type: ColumnTypeEnum) -> str:
        not_implemented_error("convert_column_type")

    @abstractmethod
    def insert_batch(self, table_name: str, records: list[Record]):
        not_implemented_error("insert_batch")
