from pathlib import Path
import unittest
from unittest.mock import MagicMock

from tests import config


from entities import FitFileWithPath
from tasks.transform_local_fit_to_gpx_handler import TransformLocalFitToGpxHandler
from services import GpxService

example_files = []

example_file_cycling = ()


class TestTransformLocalFitToGpxHandler(unittest.TestCase):
    def setUp(self):
        self.gpx_repo = MagicMock()
        self.handler = TransformLocalFitToGpxHandler(
            fit_file_repo=MagicMock(),
            gpx_file_repo=self.gpx_repo,
            gpx_service=GpxService(self.gpx_repo, cache_file=None),
            elevation_provider=MagicMock(),
        )

    def test_handle_example_fit_files_parameterized(self):
        for example_file in example_files:
            with self.subTest(
                msg=f"Example fitfile: {example_file.stem}", example_file=example_file
            ):
                self.handler.fit_file_repo.fetch_local_fit_files.return_value = [
                    FitFileWithPath(file_path=example_file)
                ]
                self.handler.gpx_file_repo.fetch_gpx_files.return_value = []

                self.handler.handle()

                self.handler.fit_file_repo.fetch_local_fit_files.assert_called_once()

                self.handler.gpx_file_repo.fetch_gpx_files.assert_called_once()
                self.handler.gpx_file_repo.save_file.assert_called_once()

                self.handler.elevation_provider.update_elevation.assert_called()

            self.setUp()

    def test_handle_other_sport_should_be_skipped(self):

        self.handler.fit_file_repo.fetch_local_fit_files.return_value = [
            FitFileWithPath(file_path=example_file_cycling)
        ]
        self.handler.gpx_file_repo.fetch_gpx_files.return_value = []

        self.handler.handle()

        self.handler.fit_file_repo.fetch_local_fit_files.assert_called_once()
        self.handler.gpx_file_repo.fetch_gpx_files.assert_called_once()

        self.handler.gpx_file_repo.save_file.assert_not_called()
        self.handler.elevation_provider.update_elevation.assert_not_called()


if __name__ == "__main__":
    unittest.main()
