import json
import logging

import requests
from pelican.readers import BaseReader
from pelican import signals
from pathlib import Path

log = logging.getLogger(__name__)
open_library_url = "https://openlibrary.org/"
headers = {
    "User-Agent": (
        "open-library-book-reviews pelican plugin "
        "https://github.com/HybridAU/open-library-book-reviews "
        "(michael@xo.tc)"
    )
}


def add_metadata_and_tags(generator, metadata):
    """Add metadata downloaded from Open Library"""
    settings = generator.settings
    # Author, category, and tags are objects, not strings, so they need to
    # be handled using BaseReader's process_metadata() function.
    base_reader = BaseReader(settings)

    if "olid" in metadata:
        book_details = fetch_book_details(metadata["olid"], settings)
        metadata["open_library_book_details"] = book_details

        if "tags" in metadata:
            metadata["tags"].extend(
                base_reader.process_metadata("tags", "Open Library")
            )
        else:
            metadata["tags"] = base_reader.process_metadata("tags", "Open Library")


def fetch_book_details(olid, settings):
    cache_dir = (
        settings.get("OPEN_LIBRARY_BOOK_REVIEWS", {}).get("cache_directory")
        or "open_library_cache"
    )
    Path(cache_dir, "books").mkdir(parents=True, exist_ok=True)
    file_path = Path(cache_dir, "books", f"{olid}.json")

    # Check for book data in cache first
    if file_path.is_file():
        book_data = json.loads(open(file_path, "r").read())
    else:
        log.warning(f"Could not find cached info downloading {olid=}")
        response = requests.get(f"{open_library_url}books/{olid}.json", headers=headers)
        if response.status_code == 200:
            book_data = response.json()
            open(file_path, "w").write(json.dumps(book_data))
        else:
            book_data = {}

    # Just return mock data until we can get the caching sorted out
    return book_data


def register():
    signals.article_generator_context.connect(add_metadata_and_tags)
