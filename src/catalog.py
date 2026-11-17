from collections.abc import Iterator

from src.errors import DuplicateError, FilmNotFound
from src.models import Film


class Catalog:

    def __init__(self) -> None:
        self.films: dict[str, Film] = {}


    def __iter__(self) -> Iterator[Film]:
        return iter(self.films.values())


    def __len__(self) -> int:
        return len(self.films)


    def __contains__(self, id: str) -> bool:
        return id in self.films


    def add(self, other: Film) -> None:
        if other.id in self.films:
            raise DuplicateError("Movie ID already exists")

        self.films[other.id] = other


    def get(self, id: str) -> Film:
        if id not in self.films:
            raise FilmNotFound("Film with this identifier was not found in the catalog")
        return self.films[id]


    def remove(self, id: str) -> None:
        if id not in self.films:
            raise FilmNotFound("Film with this identifier was not found in the catalog")
        del self.films[id]


    def find_by_category(self, category: str) -> list[Film]:
        result = []
        for film in self.films.values():
            if film.category == category:
                result.append(film)
        return result


    def find_by_name(self, name: str) -> list[Film]:
        result = []
        for film in self.films.values():
            if name.casefold() in film.name.casefold():
                result.append(film)
        return result
