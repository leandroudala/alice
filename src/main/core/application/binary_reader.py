from io import BufferedReader
from collections import deque
import struct

# key = bytes
# value = tuple (signed, float format (if applicable))
# for usigned, use Upper Case
BYTE_SIZE_SIGNED = {
    1: ("b", None),  # char
    2: ("H", "e"),  # short, half precision float (python 3.6+)
    4: ("I", "f"),  # int, single-precision float
    8: ("q", "d"),  # long, double-precision float
}

LITTLE_ENDIAN_OPERATOR = "<"
BIG_ENDIAN_OPERATOR = ">"


class BinaryReader:

    last_bytes = deque(maxlen=10)

    def __init__(self, file: BufferedReader):
        self.file = file

    """Skip files"""

    def skip(self, bytes_to_skip: int = 1) -> int:
        return self.file.seek(bytes_to_skip, 1)
    
    def __print_deque(self):
        for data in self.last_bytes:
            print(' >', data)

    def extract_value(self, operator: str, b: int):
        data = self.file.read(b)
        try:
            result = struct.unpack(operator + BYTE_SIZE_SIGNED[b][0], data)
            self.last_bytes.append(data)
            return result[0]
        except Exception as e:
            print("data:", data)
            self.__print_deque()
            print("operator:", operator + BYTE_SIZE_SIGNED[b][0])
            print("bytes:", b)
            print()
            raise e

    def next_short(self) -> int:

        return self.extract_value(LITTLE_ENDIAN_OPERATOR, 2)

    def next_int(self) -> int:
        return self.extract_value(LITTLE_ENDIAN_OPERATOR, 4)

    def read(self, size: int | None = -1):
        return self.file.read(size)
