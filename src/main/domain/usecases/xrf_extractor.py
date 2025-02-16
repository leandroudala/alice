import struct

from domain.entities.cross_reference import CrossReference, Pointer


class XRFExtractor:
    filename: str
    BLOCK_SIZE = 512
    pointers = []

    def __init__(self, filename: str):
        self.filename = filename

    def __read_block(self, offset: int = 0) -> bytes:
        with open(self.filename, mode="rb") as file:
            file.seek(offset * self.BLOCK_SIZE)
            return file.read(self.BLOCK_SIZE)

    def is_logically_deleted(self, xr_fmb: int, xr_fmp: int) -> bool:
        return xr_fmb < 0 and xr_fmp > 0

    def is_physically_deleted(self, xr_fmb: int, xr_fmp: int) -> bool:
        return xr_fmb == -1 and xr_fmp == 0

    def is_deleted(self, xr_fmb: int, xr_fmp: int) -> bool:
        """
        Special cases:
        - If XRFMFB < 0 and XRFMFP > 0: logically deleted record.
        - If XRFMFB == -1 and XRFMFP == 0: physically deleted record.
        - If both are 0: inexistent record.
        """
        return self.is_logically_deleted(xr_fmb, xr_fmp) or self.is_physically_deleted(
            xr_fmb, xr_fmp
        )

    def __check_block_size(self, block: bytes):
        """Check if the block size is exactly 512 bytes"""
        if len(block) != self.BLOCK_SIZE:
            raise ValueError("Block must be exactly 512 bytes")

    def __extract_data(self, block: bytes):
        """
        Parse a 512-byte XRF block.

        The block starts with a 4-byte XRFPOS field followed by 127 pointers (each 4 bytes).
        Each pointer is stored as a 31-bit signed integer:

            pointer = XRFMFB * 2048 + XRFMFP

        where:
        - XRFMFB (21 bits) is the Master file block number.
        - XRFMFP (11 bits) is the offset within that block.
        """

        self.__check_block_size(block)

        # Read the first 4 bytes: XRFPOS (little-endian signed 32-bit integer)
        (xr_pos,) = struct.unpack_from("<i", block, 0)
        xrf_block_number = abs(xr_pos)
        last_block = xr_pos < 0

        # Gather all 127 pointers.
        pointers = []
        for i in range(127):
            offset = 4 + i * 4
            (pointer_val,) = struct.unpack_from("<i", block, offset)

            if pointer_val == 0:
                continue

            xr_fmb = pointer_val // 2048
            xr_fmp = pointer_val - (xr_fmb * 2048)

            if self.is_deleted(xr_fmb, xr_fmp):
                continue

            status = f"Active record (Master file block {xr_fmb}, offset {xr_fmp})"

            pointers.append(
                {
                    "MFN": i + 1,  # master file number
                    "raw": pointer_val,
                    "XRFMFB": xr_fmb,  # master file block
                    "XRFMFP": xr_fmp,  # master file pointer
                    "status": status,
                }
            )

        return {
            "XRFPOS": xr_pos,
            "block_number": xrf_block_number,
            "last_block": last_block,
            "pointers": pointers,
        }

    def __to_pointer(self, raw) -> Pointer:
        record_id = raw["MFN"]
        block_number = raw["XRFMFB"]
        offset = raw["XRFMFP"]
        if offset > self.BLOCK_SIZE:
            offset -= 1024

        return Pointer(record_id, block_number, offset)

    def to_cross_reference(self) -> list[CrossReference]:
        continue_reading = True
        references: list[CrossReference] = []

        block_id = 0
        while continue_reading:
            block = self.__read_block(block_id)
            data = self.__extract_data(block)

            block_number = data["block_number"]
            last_block = data["last_block"]
            pointers = tuple(map(self.__to_pointer, data["pointers"]))

            reference = CrossReference(block_number, last_block, pointers)
            references.append(reference)
            continue_reading = not last_block
            block_id += 1

        return references
