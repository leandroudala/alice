import os
import sys

from core.usecase.fdt_extractor import FDTExtractor
from core.usecase.mst_extractor import MSTExtractor
from core.usecase.xrf_extractor import XRFExtractor
from core.domain.cross_reference import CrossReference
from core.domain.master_file import Record
from core.domain.table_definition import ColumnDefinition

database = "CDS"
extension_upper = True  # linux is case sensitive


def get_file(extension: str) -> str:
    global extension_upper, database
    extension = extension.upper() if extension_upper else extension.lower()
    return "sample/%s.%s" % (database, extension)


def extract_cross_references() -> list[CrossReference]:
    # Processing XRF File
    xrf_file = get_file("xrf")
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


def extract_master_file() -> MSTExtractor:
    # Processing MST File
    mst_file = get_file("mst")
    return MSTExtractor(mst_file)


def show_menu():
    print("Escolha uma das opções abaixo:")
    print("1 - Gerar SQLite a partir de dados do CDS/ISIS")
    print("0 - Sair")
    print()

    return input("> ")


def etl():
    cross_references = extract_cross_references()
    mst_extractor = extract_master_file()

    total_records: list[Record] = []
    for reference in cross_references:
        pointers = reference.pointers
        for pointer in pointers:
            processed = mst_extractor.extract_data(pointer)
            total_records.append(processed)

    print("Database: %s, records: %d" % (database, len(total_records)))
    print()


def exit_system():
    os.system('clear')
    print('Encerrando...')
    sys.exit(0)


MENU_OPTIONS = [
    exit_system,
    etl
]

def run_app():
    while True:
        try:
            selected = int(show_menu())
            MENU_OPTIONS[selected]()
        except Exception:
            os.system('clear')
            print("Opção desconhecida:", selected, '\n')


if __name__ == "__main__":
    run_app()
