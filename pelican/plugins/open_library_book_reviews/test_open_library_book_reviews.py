import unittest
from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp

from pelican.settings import read_settings

from pelican import Pelican

from . import open_library_book_reviews

BASE_DIR = Path(".").resolve()
TEST_DATA = BASE_DIR / "pelican/plugins/open_library_book_reviews/test_data"


class TestOpenLibraryPlugin(unittest.TestCase):
    """Test class for Open Library plugin."""

    def setUp(self):
        self.output_path = mkdtemp(prefix="pelican-plugins-open-library-tests-")

    def tearDown(self):
        rmtree(self.output_path)

    def _run_pelican(self):
        settings = read_settings(
            override={
                "CACHE_CONTENT": False,
                "SITEURL": "http://localhost",
                "PATH": TEST_DATA,
                "OUTPUT_PATH": self.output_path,
                "PLUGINS": [open_library_book_reviews],
            }
        )
        pelican = Pelican(settings=settings)
        pelican.run()

    def test_adds_open_library_tag(self):
        """Just a simple test to get something going."""
        self._run_pelican()
        with open(Path(self.output_path) / "night-watch.html") as night_watch_review:
            contents = night_watch_review.read()
            self.assertIn("Open Library", contents)
