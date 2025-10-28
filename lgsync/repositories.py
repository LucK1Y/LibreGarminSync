from pathlib import Path
from shutil import copyfile
from typing import List
from fitparse import FitFile
from gpxpy.gpx import GPX
import srtm
from Interfaces import (
    IGpxFileRepository,
    IFitFileRepository,
    IElevationProvider,
)
from entities import FitFileWithPath, GpxWithPath


class GpxFileRepository(IGpxFileRepository):
    def __init__(self, gpx_directory: Path):
        self.gpx_directory = gpx_directory

        if not self.gpx_directory.exists():
            self.gpx_directory.mkdir(parents=True, exist_ok=True)

    def save_file(self, gpx: GpxWithPath, filename: str) -> None:
        with open(self.gpx_directory / filename, "w") as f:
            f.write(gpx.gpx.to_xml())

    def file_with_key_exists(self, key: str) -> bool:
        return any(self.gpx_directory.glob(f"*{key}*"))

    def fetch_gpx_files(self) -> List[GpxWithPath]:
        files = []
        for gpx_file in self.gpx_directory.glob("*.gpx"):
            files.append(GpxWithPath(file_path=gpx_file))
        return files


class FitFileRepository(IFitFileRepository):
    def __init__(self, local_fit_directory: Path, remote_fit_directory: Path):
        self.local_fit_directory = local_fit_directory
        self.remote_fit_directory = remote_fit_directory

        if not self.local_fit_directory.exists():
            print("Warning: LOCAL Fit directory does not exist. Creating it.")
            self.local_fit_directory.mkdir(parents=True, exist_ok=True)

        if not self.remote_fit_directory.exists():
            print(
                "Warning: REMOTE Fit directory does not exist. Maybe watch is not connected."
            )

    def __fetch_fit_files_from_dir(self, base_directory: Path) -> List[FitFileWithPath]:
        if not base_directory.exists():
            raise FileNotFoundError(f"Fit directory {base_directory} does not exist.")

        files = []
        for fit_file in base_directory.glob("*.FIT", case_sensitive=False):
            files.append(FitFileWithPath(fit_file))
        return files

    def fetch_remote_fit_files(self) -> List[FitFileWithPath]:
        return self.__fetch_fit_files_from_dir(self.remote_fit_directory)

    def fetch_local_fit_files(self) -> List[FitFileWithPath]:
        return self.__fetch_fit_files_from_dir(self.local_fit_directory)

    def copy_file_to_local_if_not_exist(self, remote_file_path: Path) -> Path:
        new_file_path = self.local_fit_directory / remote_file_path.name
        if new_file_path.exists():
            print(f"File {new_file_path} already exists. Skipping copy.")
            return new_file_path

        copyfile(remote_file_path, new_file_path)
        return new_file_path


class SRMTElevationProvider(IElevationProvider):
    def update_elevation(self, gpx: GPX) -> GPX:
        elevation_data = srtm.get_data(srtm1=False)
        elevation_data.add_elevations(
            gpx, smooth=True, gpx_smooth_no=30, only_missing=True
        )
        return gpx


class SWISSAPIElevationProvider(IElevationProvider):
    def update_elevation(self, gpx: GPX) -> GPX:
        # Todo
        raise NotImplementedError("SWISS API elevation provider not implemented yet.")
