from core.application.xrf_extractor import XRFExtractor
from core.application.mst_extractor import MSTExtractor
from core.application.fdt_extractor import FDTExtractor

database = "DOC"
extension_upper = False


def get_file(extension: str) -> str:
    global extension_upper, database
    return "data/%s.%s" % (
        database,
        extension.upper() if extension_upper else extension.lower(),
    )


cross_reference = None
xrf_file = get_file("xrf")

xrf_extractor = XRFExtractor(xrf_file)
cross_reference = xrf_extractor.to_cross_reference()

mst_file = get_file("mst")
print(cross_reference)
mst_extractor = MSTExtractor(mst_file)

for pointer in cross_reference.pointers:
    processed = mst_extractor.extract_data(pointer)
    print(processed)
    print()

fdt_file = get_file("fdt")
fdt_extractor = FDTExtractor(fdt_file)
columns = fdt_extractor.extract_data()

for column in columns:
    print(column)

print("Columns found", len(columns))
