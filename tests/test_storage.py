import json
from dataclasses import asdict
from pathlib import Path

import pytest

from src.catalog import Catalog
from src.constants import FIRST_FORMAT_VERSION
from src.errors import CorruptedFileError, UnsupportedVersionError
from src.models import Film
from src.storage import export, load


@pytest.fixture
def film() -> Film:
    return Film("1", "Shutter Island", "Thriller", 2010, "Martin Scorsese", 138, 99)


@pytest.fixture
def second_film() -> Film:
    return Film("2", "Inception", "Sci-Fi", 2010, "Christopher Nolan", 148, 95)


def test_export_and_load(tmp_path: Path, film: Film, second_film: Film) -> None:
    catalog = Catalog()
    catalog.add(second_film)
    catalog.add(film)
    path = tmp_path / "films.json"

    export(catalog, str(path))

    loaded = Catalog()
    load(loaded, str(path))

    assert list(loaded) == [second_film, film]


def test_load_adds_to_existing_catalog(tmp_path: Path, film: Film, second_film: Film) -> None:
    catalog = Catalog()
    catalog.add(film)

    source = Catalog()
    source.add(second_film)
    path = tmp_path / "films.json"
    export(source, str(path))

    load(catalog, str(path))

    assert list(catalog) == [film, second_film]


def test_load_broken_json(tmp_path: Path) -> None:
    path = tmp_path / "films.json"
    path.write_text("{", encoding="utf-8")

    with pytest.raises(CorruptedFileError):
        load(Catalog(), str(path))


def test_load_unsupported_version(tmp_path: Path) -> None:
    path = tmp_path / "films.json"
    data = {"format_version": FIRST_FORMAT_VERSION + 1, "films": []}
    path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(UnsupportedVersionError):
        load(Catalog(), str(path))


def test_load_invalid_film_leaves_catalog_unchanged(tmp_path: Path, film: Film, second_film: Film) -> None:
    catalog = Catalog()
    catalog.add(film)
    path = tmp_path / "films.json"

    # put a valid film before the invalid one to catch partial loading
    data = {
        "format_version": FIRST_FORMAT_VERSION,
        "films": [asdict(second_film), {"id": "3"}],
    }
    path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(CorruptedFileError):
        load(catalog, str(path))

    assert list(catalog) == [film]


def test_load_duplicate_id_leaves_catalog_unchanged(tmp_path: Path, film: Film, second_film: Film) -> None:
    catalog = Catalog()
    catalog.add(film)

    source = Catalog()
    # the first film has a new id, the second conflicts with the catalog
    source.add(second_film)
    source.add(film)
    path = tmp_path / "films.json"
    export(source, str(path))

    with pytest.raises(CorruptedFileError):
        load(catalog, str(path))

    assert list(catalog) == [film]
