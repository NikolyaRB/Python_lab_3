import pytest

from src.errors import InvalidFilmError
from src.models import Film


def test_valid_film() -> None:
    film = Film(
        id="1",
        name="Shutter Island",
        category="Thriller",
        year=2010,
        director="Martin Scorsese",
        duration=138,
        rating=99,
    )

    assert film.id == "1"
    assert film.name == "Shutter Island"
    assert film.category == "Thriller"
    assert film.year == 2010
    assert film.director == "Martin Scorsese"
    assert film.duration == 138
    assert film.rating == 99


@pytest.mark.parametrize("value", ["", "   ", 1, None, True])
@pytest.mark.parametrize("field", ["id", "name", "category", "director"])
def test_invalid_text_field(field, value) -> None:
    data = {
        "id": "1",
        "name": "Shutter Island",
        "category": "Thriller",
        "year": 2010,
        "director": "Martin Scorsese",
        "duration": 138,
        "rating": 99,
    }

    # replace one field with an invalid value
    data[field] = value

    with pytest.raises(InvalidFilmError):
        Film(**data)


@pytest.mark.parametrize("value", [0, -1, "2010", 2010.5, None, True, False])
def test_invalid_year(value) -> None:
    with pytest.raises(InvalidFilmError):
        Film("1", "Shutter Island", "Thriller", value, "Martin Scorsese", 138, 99)


@pytest.mark.parametrize("value", [0, -1, "138", 138.5, None, True, False])
def test_invalid_duration(value) -> None:
    with pytest.raises(InvalidFilmError):
        Film("1", "Shutter Island", "Thriller", 2010, "Martin Scorsese", value, 99)


@pytest.mark.parametrize("value", [-1, 101, "99", 99.5, None, True, False])
def test_invalid_rating(value) -> None:
    with pytest.raises(InvalidFilmError):
        Film("1", "Shutter Island", "Thriller", 2010, "Martin Scorsese", 138, value)


@pytest.mark.parametrize("value", [0, 100])
def test_rating_boundaries(value) -> None:
    film = Film("1", "Shutter Island", "Thriller", 2010, "Martin Scorsese", 138, value)

    assert film.rating == value
