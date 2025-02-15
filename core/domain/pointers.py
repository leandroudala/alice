class Pointer:
    id: int
    offset: int
    block_number: int

    def __init__(self, id: int, block_number: int, offset: int):
        self.id = id
        self.block_number = block_number
        self.offset = offset

    def __str__(self) -> str:
        return '{"id":%d,"block_number":%d,"offset":%d}' % (
            self.id,
            self.block_number,
            self.offset,
        )


class CrossReference:
    block_number: int
    is_last_block: bool
    pointers: list[Pointer]

    def __init__(self, block_number: int, is_last_block: bool, pointers: list[Pointer]):
        self.block_number = block_number
        self.is_last_block = is_last_block
        self.pointers = pointers

    def __str__(self) -> str:
        return '{"block_number":%d,"is_last_block":%d,"pointers":[%s]}' % (
            self.block_number,
            self.is_last_block,
            ",".join(str(pointer) for pointer in self.pointers),
        )
