from pathlib import Path
from tempfile import TemporaryDirectory

from src.catalog import Catalog
from src.models import Film
from src.storage import export, load


def main() -> None:
    catalog = Catalog()
    film = Film("1", "Shutter Island", "Thriller", 2010, "Martin Scorsese", 138, 99)
    catalog.add(film)

    print(f"Films in catalog: {len(catalog)}")

    if len(catalog) != 0:
        print("Search results:")



    for found in catalog.find_by_name("island"):
        print(f"{found.name} ({found.year})")

    # save to a temporary file and load into a new catalog
    with TemporaryDirectory() as directory:
        path = str(Path(directory) / "films.json")
        export(catalog, path)

        loaded_catalog = Catalog()
        load(loaded_catalog, path)

    print("Loaded films:")
    for loaded_film in loaded_catalog:
        print(f"{loaded_film.name} ({loaded_film.year})")


if __name__ == "__main__":
    main()
