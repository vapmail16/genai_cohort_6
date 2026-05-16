"""Sanity checks for monorepo-relative paths used by test_openai."""

import unittest
from pathlib import Path


class TestEnvPaths(unittest.TestCase):
    def test_openai_folder_resolves_under_repo_root(self) -> None:
        here = Path(__file__).resolve().parent
        root = here.parent
        self.assertEqual(here.name, "openai_api_test")
        self.assertTrue((root / "README.md").is_file())
        self.assertTrue((here / "test_openai.py").is_file())


if __name__ == "__main__":
    unittest.main()
