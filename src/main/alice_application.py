from core.application.fdt_extractor import FDTExtractor
from core.application.mst_extractor import MSTExtractor
from core.application.xrf_extractor import XRFExtractor
from core.domain.cross_reference import CrossReference
from core.domain.table_definition import ColumnDefinition
from core.domain.master_file import Record

database = "THES"
extension_upper = True  # linux is case sensitive


def get_file(extension: str) -> str:
    global extension_upper, database
    extension = extension.upper() if extension_upper else extension.lower()
    return "sample/%s.%s" % (database, extension)


def extract_cross_references() -> list[CrossReference]:
    xrf_extractor = XRFExtractor(xrf_file)
    return xrf_extractor.to_cross_reference()


def extract_field_table_definition() -> ColumnDefinition:
    # Processing FDT File
    fdt_file = get_file("fdt")

    fdt_extractor = FDTExtractor(fdt_file)
    columns = fdt_extractor.extract_data()

    for column in columns:
        print(column)

    print("Columns found", len(columns))


# Processing XRF File
cross_reference = None
xrf_file = get_file("xrf")

cross_references = extract_cross_references()

# Processing MST File
mst_file = get_file("mst")
mst_extractor = MSTExtractor(mst_file)


total_records: list[Record] = []
for reference in cross_references:
    pointers = reference.pointers
    for pointer in pointers:
        processed = mst_extractor.extract_data(pointer)
        total_records.append(processed)


print("Database: %s, records: %d" % (database, len(total_records)))
