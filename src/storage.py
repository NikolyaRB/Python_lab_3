import json
from dataclasses import asdict

from src.catalog import Catalog
from src.constants import FIRST_FORMAT_VERSION
from src.errors import (
    CatalogError,
    CorruptedFileError,
    DuplicateError,
    UnsupportedVersionError,
)
from src.models import Film


def export(catalog: Catalog, path: str) -> None:
    # convert films to dictionaries and add the format version
    data = {
        "format_version": FIRST_FORMAT_VERSION,
        "films": [asdict(film) for film in catalog],
    }

    # open the file and write data
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except OSError as error:
        raise CorruptedFileError(f"Cannot save catalog to '{path}': {error}") from error


def load(catalog: Catalog, path: str) -> None:
    # read data from the file
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError, UnicodeError) as error:
        raise CorruptedFileError(f"Cannot read catalog from '{path}': {error}") from error

    # check the file structure and format version
    if type(data) is not dict:
        raise CorruptedFileError("JSON root must be an object")

    if "format_version" not in data:
        raise CorruptedFileError("Missing format_version")

    if type(data["format_version"]) is not int:
        raise CorruptedFileError("format_version must be an number")

    if data["format_version"] != FIRST_FORMAT_VERSION:
        raise UnsupportedVersionError("Unsupported format version")

    if "films" not in data or type(data["films"]) is not list:
        raise CorruptedFileError("Films must be a list")

    # store new films separately to keep the catalog unchanged on error
    temporary_catalog = Catalog()

    for film_data in data["films"]:
        if type(film_data) is not dict:
            raise CorruptedFileError("Each film must be an object")

        try:
            film = Film(**film_data)

            # check for an existing id in the original catalog
            if film.id in catalog:
                raise DuplicateError("Movie ID already exists")

            temporary_catalog.add(film)
        except (TypeError, CatalogError) as error:
            raise CorruptedFileError(f"Invalid film data: {error}") from error

    # add films after all checks pass
    for film in temporary_catalog:
        catalog.add(film)
