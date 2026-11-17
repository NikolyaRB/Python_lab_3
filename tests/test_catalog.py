import pytest

from src.catalog import Catalog
from src.errors import DuplicateError, FilmNotFound
from src.models import Film


@pytest.fixture
def film() -> Film:
    return Film("1", "Shutter Island", "Thriller", 2010, "Martin Scorsese", 138, 99)


def test_add_get_and_remove(film: Film) -> None:
    catalog = Catalog()

    catalog.add(film)
    assert len(catalog) == 1
    assert film.id in catalog
    assert catalog.get(film.id) == film

    catalog.remove(film.id)
    assert len(catalog) == 0
    assert film.id not in catalog


def test_duplicate_id(film: Film) -> None:
    catalog = Catalog()
    catalog.add(film)
    duplicate = Film(film.id, "Inception", "Sci-Fi", 2010, "Christopher Nolan", 148, 95)

    with pytest.raises(DuplicateError):
        catalog.add(duplicate)

    assert catalog.get(film.id) == film


def test_get_missing_film() -> None:
    catalog = Catalog()

    with pytest.raises(FilmNotFound):
        catalog.get("missing")


def test_remove_missing_film() -> None:
    catalog = Catalog()

    with pytest.raises(FilmNotFound):
        catalog.remove("missing")


def test_find_by_category(film: Film) -> None:
    catalog = Catalog()
    catalog.add(film)
    catalog.add(Film("2", "Inception", "Sci-Fi", 2010, "Christopher Nolan", 148, 95))

    assert catalog.find_by_category("Thriller") == [film]
    assert catalog.find_by_category("Comedy") == []


def test_find_by_name(film: Film) -> None:
    catalog = Catalog()
    catalog.add(film)
    catalog.add(Film("2", "Inception", "Sci-Fi", 2010, "Christopher Nolan", 148, 95))

    assert catalog.find_by_name("iSLaNd") == [film]
    assert catalog.find_by_name("unknown") == []


def test_iteration_order(film: Film) -> None:
    catalog = Catalog()
    second = Film("2", "Inception", "Sci-Fi", 2010, "Christopher Nolan", 148, 95)

    # add films in reverse id order to verify insertion order
    catalog.add(second)
    catalog.add(film)

    assert list(catalog) == [second, film]
