import os
import sys

from domain.usecases.fdt_extractor import FDTExtractor
from domain.usecases.mst_extractor import MSTExtractor
from domain.usecases.xrf_extractor import XRFExtractor
from domain.entities.cross_reference import CrossReference
from domain.entities.master_file import Record
from domain.entities.table_definition import ColumnDefinition
from domain.usecases.fdt_to_database import FTDToDatabase
from infrastructure.database.sqlite_db import SQLiteDatabase

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


def extract_field_table_definition() -> list[ColumnDefinition]:
    # Processing FDT File
    fdt_file = get_file("fdt")

    fdt_extractor = FDTExtractor(fdt_file)
    columns = fdt_extractor.extract_data()

    return columns


def extract_master_file() -> MSTExtractor:
    # Processing MST File
    mst_file = get_file("mst")
    return MSTExtractor(mst_file)


def show_menu():
    print("Escolha uma das opções abaixo:")
    print("1 - Criar banco de dados")
    print("2 - Gerar SQLite a partir de dados do CDS/ISIS")
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
    os.system("clear")
    print("Encerrando...")
    sys.exit(0)


def create_db():
    print("\nCriando tabela")
    columns = extract_field_table_definition()
    db = SQLiteDatabase(database)
    db_creator = FTDToDatabase(db)
    db_creator.create_table("cds", columns)


MENU_OPTIONS = [exit_system, create_db, etl]


def run_app():
    while True:
        try:
            value = show_menu()
            selected = int(value)
            MENU_OPTIONS[selected]()
        except ValueError:
            print('Opção inválida:', value, '\n\n')

if __name__ == "__main__":
    run_app()
