# About this project

This is a simple film catalog in Python. You can add, get, and remove films by ID, or search by category or title.

## Films

Each film has a unique string ID, a title, a category, a release year, a director, a duration in minutes, and an integer rating from 0 to 100.

Categories are plain text, such as `Thriller` and `Sci-Fi`. Category search requires an exact match. Title search matches part of the title and ignores letter case. Films are listed in the order they were added.

## Storage

The catalog can be saved as JSON with a `format_version` field. Loading adds films to the existing catalog. If the file is invalid, the version is unsupported, or an ID is duplicated, the catalog stays unchanged.
