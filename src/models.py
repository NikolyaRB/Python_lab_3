from dataclasses import dataclass

from src.errors import InvalidFilmError


@dataclass
class Film:
    id: str
    name: str
    category: str
    year: int
    director: str
    duration: int
    rating: int

    def __post_init__(self) -> None:
        if type(self.id) is not str or not self.id.strip():
            raise InvalidFilmError("ID must be a non-empty string")

        if type(self.name) is not str or not self.name.strip():
            raise InvalidFilmError("Name must be a non-empty string")

        if type(self.category) is not str or not self.category.strip():
            raise InvalidFilmError("Category must be a non-empty string")

        if type(self.director) is not str or not self.director.strip():
            raise InvalidFilmError("Director must be a non-empty string")

        if type(self.year) is not int or self.year <= 0:
            raise InvalidFilmError("Year must be a positive number")

        if type(self.duration) is not int or self.duration <= 0:
            raise InvalidFilmError("Duration must be a positive number")

        if type(self.rating) is not int or not (0 <= self.rating and self.rating <= 100):
            raise InvalidFilmError("Rating must be a number from 0 to 100")
