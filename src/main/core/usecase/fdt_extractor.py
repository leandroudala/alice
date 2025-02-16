from core.domain.table_definition import column_type_to_enum, ColumnDefinition


class FDTExtractor:
    filename: str

    def __init__(self, filename: str):
        self.filename = filename

    def extract_data(self) -> list[ColumnDefinition]:
        lines: list[str] = []
        with open(self.filename, mode="r", encoding="cp850") as file:
            lines = file.readlines()
            if not len(lines):
                raise ImportError("Empty file")

        return self.__process_lines(lines)

    def __process_lines(self, lines) -> list[ColumnDefinition]:
        # removing first 4 lines
        lines = lines[4:]

        columns: list[ColumnDefinition] = []

        for line in lines:
            column = self.__line_to_column(line)
            columns.append(column)

        return columns

    def __line_to_column(self, line: str) -> ColumnDefinition:
        line = self.__prepare_line(line)

        # extracting data
        name = self.__extract_column(line)
        subfields = self.__extract_subfields(line)
        numbers = self.__extract_numbers(line)

        tag = numbers[0]
        column_type = numbers[2]
        repeat = numbers[3]

        return ColumnDefinition(
            tag, name, column_type_to_enum(column_type), subfields, repeat
        )

    def __prepare_line(self, line: str) -> str:
        return line.strip("\n")

    def __extract_column(self, line: str) -> str:
        """Column names starts at index 0 and has a length of 30 characters"""
        return line[:30].strip()

    def __extract_subfields(self, line: str) -> str:
        """Subfields starts at index 30 and has a length of 20 characters"""
        return line[30:50].strip()

    def __extract_numbers(self, line: str) -> list[int]:
        """
        Numbers starts at position 50 to the end of the line
        it has the following data:
        - tag
        - column type
        - (unknown)
        - repeat (same record could have more than one values with this tag)
        """
        line = line[50:]
        numbers = line.split(" ")
        return [int(number) for number in numbers]
