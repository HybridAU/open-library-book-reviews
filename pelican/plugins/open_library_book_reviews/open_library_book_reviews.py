import logging

import requests
from pelican.readers import BaseReader

from pelican import signals

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
        book_details = fetch_book_details(metadata["olid"])
        metadata["open_library_book_details"] = book_details

    if "tags" in metadata:
        metadata["tags"].extend(base_reader.process_metadata("tags", "Open Library"))
    else:
        metadata["tags"] = base_reader.process_metadata("tags", "Open Library")


def fetch_book_details(OLID):
    mock_data = {
        "title": "The Vexed Generation",
        "publish_date": "2019",
        "publishers": ["Rocket Hat Industries"],
        "type": {"key": "/type/edition"},
        "isbn_13": ["9781950056026"],
        "isbn_10": ["1950056023"],
        "series": ["Magic 2.0"],
        "key": "/books/OL32222701M",
        "works": [{"key": "/works/OL22598730W"}],
        "covers": [13233209],
        "source_records": ["amazon:1950056023"],
        "latest_revision": 5,
        "revision": 5,
        "created": {"type": "/type/datetime", "value": "2021-04-20T09:14:26.394088"},
        "last_modified": {
            "type": "/type/datetime",
            "value": "2023-02-03T16:17:42.318825",
        },
    }
    # response = requests.get(f"{open_library_url}books/{OLID}.json", headers=headers)
    # if response.status_code == 200:
    #     return response.json()

    # Just return mock data until we can get the caching sorted out
    return mock_data


def register():
    signals.article_generator_context.connect(add_metadata_and_tags)
