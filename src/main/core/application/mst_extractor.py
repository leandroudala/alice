from functools import reduce
import struct
from io import BufferedReader

from core.domain.master_file import Field, Record
from core.domain.pointers import Pointer


BLOCK_SIZE = 512


def to_int(raw: bytes) -> int:
    return int.from_bytes(raw, "little")


def next_short(file: BufferedReader) -> int:
    return to_int(file.read(2))


def next_int(file: BufferedReader) -> int:
    return to_int(file.read(4))


def skip(file: BufferedReader, offset: int):
    file.seek(offset, 1)


def next_chunk(file: BufferedReader, offset: int):
    return file.read(offset)


class MSTExtractor:
    filename: str
    file: BufferedReader

    def __init__(self, filename: str):
        self.filename = filename

    def __calculate_absolute_offset(self, pointer: Pointer) -> int:
        block_offset = (pointer.block_number - 1) * BLOCK_SIZE
        return block_offset + pointer.offset

    def extract_data(self, pointer: Pointer):
        """
        Given a pointer value (computed as XRFMFB * 2048 + XRFMFP)
        from the XRF table, extract the corresponding record from the MST file.

        This example assumes the MST record starts with a 4-byte little-endian unsigned
        integer indicating the record length, immediately followed by the record data.
        """
        absolute_offset = self.__calculate_absolute_offset(pointer)

        return self.__read_file(absolute_offset)

    def __calculate_fields_bytes(self, fields: int) -> int:
        return fields * 6

    def __process_fields(self, quantity_fields: int, raw: bytes) -> list[Field]:
        fields: list[Field] = []

        for i in range(0, quantity_fields):
            position = i * 6
            field_id = to_int(raw[0 + position : 2 + position])
            start = to_int(raw[2 + position : 4 + position])
            length = to_int(raw[4 + position : 6 + position])
            fields.append(Field(field_id, start, length))

        return fields

    def __read_file(self, absolute_offset: int):
        # The pointer directly gives the offset into the MST file.
        with open(self.filename, "rb") as f:
            f.seek(absolute_offset)

            # Read the first 4 bytes to get the record length.
            record_id = next_int(f)
            # skipping 10 unnecessary bytes
            skip(f, 10)
            number_of_fields = next_short(f)

            # skipping 2 uncessary bytes (status)
            skip(f, 2)
            fields_size = self.__calculate_fields_bytes(number_of_fields)
            fields_raw = next_chunk(f, fields_size)
            fields = self.__process_fields(number_of_fields, fields_raw)
            chunk_size = sum(f.length for f in fields)

            chunk = next_chunk(f, chunk_size)
            return Record(record_id, fields, chunk)
