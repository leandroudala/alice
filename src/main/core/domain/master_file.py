ENCODING = "cp850"


class Field:
    id: int
    start: int
    length: int

    def __init__(self, id: int, start: int, length: int):
        self.id = id
        self.start = start
        self.length = length

    def __str__(self) -> str:
        return '{"id":%d,"start":%d,"length":%d}' % (self.id, self.start, self.length)


class Record:
    id: int
    fields: list[Field]
    data: dict

    def __init__(self, id: int, fields: list[Field], chunk: bytes):
        self.id = id
        self.fields = fields
        self.data = {}

        self.__process_chunk(chunk)

    def __process_chunk(self, chunk: bytes):
        text = chunk.decode(ENCODING)
        for field in self.fields:
            value = text[field.start : field.start + field.length]
            self.__add_data(field.id, value)

    def __add_data(self, id: int, value: str):
        if id in self.data:
            self.data[id] = [self.data[id], value]
        else:
            self.data[id] = value

    def __str__(self) -> str:
        return '{"id":%d,"fields":[%s],"data":{%s}}' % (
            self.id,
            [str(field) for field in self.fields],
            str(self.data)
        )
