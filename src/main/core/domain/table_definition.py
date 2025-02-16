from enum import Enum


class ColumnTypeEnum(Enum):
    ALPHANUMERIC = 0
    ALPHABETIC = 1
    NUMERIC = 2
    PATTERN = 3


def column_type_to_enum(column_type: int) -> ColumnTypeEnum:
    return ColumnTypeEnum(column_type)


class ColumnDefinition:
    tag: int
    name: str
    column_type: ColumnTypeEnum
    subfields: str
    repeat: bool

    def __init__(
        self,
        tag: int,
        name: str,
        column_type: ColumnTypeEnum,
        subfields: str,
        repeat: bool,
    ):
        self.tag = tag
        self.name = name
        self.column_type = column_type
        self.subfields = subfields
        self.repeat = repeat

    def __str__(self) -> str:
        return (
            '{"tag":%d,"name":"%s","columnType":"%s","subfields":"%s","repeat":%i}'
            % (self.tag, self.name, self.column_type.name, self.subfields, self.repeat)
        )
