import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

import main


class URLShortenerTests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_file = Path(self.temp_dir.name) / "urls.json"

        self.original_data_file = main.DATA_FILE
        main.DATA_FILE = self.data_file

    def tearDown(self):
        main.DATA_FILE = self.original_data_file
        self.temp_dir.cleanup()

    def test_valid_url(self):
        self.assertEqual(
            main.normalize_url("https://example.com/page"),
            "https://example.com/page",
        )

    def test_invalid_url(self):
        with self.assertRaises(ValueError):
            main.normalize_url("example.com")

    def test_shorten_and_resolve(self):
        args = Namespace(
            url="https://example.com",
            alias=None,
        )

        self.assertEqual(main.cmd_shorten(args), 0)

        code = next(iter(main.load_data()))

        resolve_args = Namespace(
            code=code,
            open=False,
        )

        self.assertEqual(main.cmd_resolve(resolve_args), 0)

        self.assertEqual(
            main.load_data()[code]["clicks"],
            1,
        )

    def test_duplicate_url(self):
        args = Namespace(
            url="https://example.com",
            alias=None,
        )

        main.cmd_shorten(args)
        main.cmd_shorten(args)

        self.assertEqual(len(main.load_data()), 1)

    def test_custom_alias(self):
        args = Namespace(
            url="https://github.com/",
            alias="github",
        )

        self.assertEqual(main.cmd_shorten(args), 0)

        self.assertIn(
            "github",
            main.load_data(),
        )

    def test_duplicate_alias(self):
        first = Namespace(
            url="https://github.com/",
            alias="github",
        )

        second = Namespace(
            url="https://python.org/",
            alias="github",
        )

        self.assertEqual(main.cmd_shorten(first), 0)
        self.assertEqual(main.cmd_shorten(second), 2)

        self.assertEqual(len(main.load_data()), 1)

    def test_missing_code(self):
        args = Namespace(
            code="missing",
            open=False,
        )

        self.assertEqual(
            main.cmd_resolve(args),
            1,
        )


if __name__ == "__main__":
    unittest.main()