import logging

from pelican import signals
from pelican.generators import ArticlesGenerator
from pelican.readers import BaseReader

log = logging.getLogger(__name__)


def add_metadata_and_tags(article_generator: ArticlesGenerator):
    settings = article_generator.settings

    # Author, category, and tags are objects, not strings, so they need to
    # be handled using BaseReader's process_metadata() function.
    base_reader = BaseReader(settings)

    for article in article_generator.articles:
        if "openlibrary" in article.metadata.keys():
            log.warning(f"Adding tags and metadata to {article=}")
            if hasattr(article, "tags"):
                article.tags.extend(
                    base_reader.process_metadata("tags", "Open Library")
                )
            else:
                article.tags = base_reader.process_metadata("tags", "Open Library")


def register():
    signals.article_generator_pretaxonomy.connect(add_metadata_and_tags)
