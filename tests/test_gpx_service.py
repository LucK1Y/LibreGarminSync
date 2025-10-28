from pathlib import Path
import unittest
from unittest.mock import MagicMock

from tests import config


from entities import FitFileWithPath
from services import GpxService
from Interfaces import IGpxFileRepository


class TestGpxService(unittest.TestCase):
    def setUp(self):
        # Create a mock repository
        self.mock_repo = MagicMock(spec=IGpxFileRepository)
        self.gpx_service = GpxService(self.mock_repo, cache_file=None)

    def test_filter_fit_files_already_existing_as_gpx_files(self):
        # Arrange
        fit_files = [
            FitFileWithPath(Path("file1.fit")),
            FitFileWithPath(Path("file2.fit")),
            FitFileWithPath(Path("file3.fit")),
        ]
        gpx_files = [
            FitFileWithPath(Path("file1_something_else.gpx")),
            FitFileWithPath(Path("file2_another_string.gpx")),
        ]
        self.mock_repo.fetch_gpx_files.return_value = gpx_files

        # Act
        result = self.gpx_service.filter_fit_files_already_existing_as_gpx_files(
            fit_files
        )

        # Assert
        expected_result = [
            fit_files[2]
        ]  # Only file3.fit does not have a corresponding gpx
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
