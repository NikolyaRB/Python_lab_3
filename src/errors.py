class CatalogError(Exception):
    pass


class InvalidFilmError(CatalogError):
    pass


class DuplicateError(CatalogError):
    pass


class FilmNotFound(CatalogError):
    pass


class UnsupportedVersionError(CatalogError):
    pass


class CorruptedFileError(CatalogError):
    pass
