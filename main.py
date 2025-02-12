from enum import Enum
from core.application.binary_reader import BinaryReader

# File header
CTLMFN = 4  # starts with 4 bytes zero
NXTMFN = 4  # next record value
IGNORED_BYTES = 56

# Leader format
MFN = 4  # Master file number
MFRL = 2  # record length
MFBWB = 4  # Backward pointer - Block number
MFBWP = 2  # Backward pointer - Offset
BASE = 2  # Offset to variable fields (length of the Leader + Directory part)
NVF = 2  # number of fields in the record
STATUS = 2  # 0 active, 1 deleted

# Directory format
TAG = 2
POS = 2
LEN = 2


class Encoding(Enum):
    CP_437 = "cp437"
    ISO_8859_1 = "iso-8859-1"
    WINDOWS_1252 = "windows-1252"
    CP_850 = "cp850"


def extract_data(reader: BinaryReader):
    row = {}
    # reading next two bytes
    master_file_number = reader.next_int()
    row["id"] = master_file_number

    record_length = reader.next_short()
    row["length"] = record_length

    reader.skip(MFBWB + MFBWP + BASE)

    number_of_fields = reader.next_short()
    fields = []
    row["fields"] = {"len": number_of_fields, "data": fields}

    deleted = reader.next_short()
    row["deleted"] = deleted == 1

    # extracting fields
    for i in range(0, number_of_fields):
        tag = reader.next_short()
        reader.skip(2)  # skipping start index of content
        length = reader.next_short()
        field = [tag, length]
        fields.append(field)

    # joining field with values
    for index in range(0, len(fields)):
        field = fields[index]
        tag, length = field
        chunk = reader.read(length)
        text = chunk.decode(Encoding.CP_850.value)
        field.append(text)

    return row


records = []

with open("data/DOC.mst", "rb") as file:

    reader = BinaryReader(file)
    # skipping first 4 bytes
    reader.skip(CTLMFN)

    next_record = reader.next_int()
    print("Last record:", next_record)

    # skipping ignored bytes
    reader.skip(IGNORED_BYTES)

    for i in range(0, next_record):
        print(i)
        row = extract_data(reader)
        print(row)


for record in records:
    print(record)
# with open("output.txt", "w", encoding="UTF-8") as writer:
#     for field in fields:
#         tag, _, chunk = field
#         text = chunk.decode(Encoding.CP_850.value)
#         writer.write(str(tag) + " " + text + "\n")
