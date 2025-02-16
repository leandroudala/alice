from core.application.xrf_extractor import XRFExtractor
from core.application.mst_extractor import MSTExtractor


cross_reference = None
xrf_file = "data/DOC.xrf"

xrf_extractor = XRFExtractor(xrf_file)
cross_reference = xrf_extractor.to_cross_reference()

mst_file = "data/DOC.mst"
print(cross_reference)
mst_extractor = MSTExtractor(mst_file)

for pointer in cross_reference.pointers:
    processed = mst_extractor.extract_data(pointer)
    print(processed)
    print()