from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
from gpxpy.gpx import GPX
import pandas as pd
from entities import FitFileWithPath, GpxWithPath, Settings


class IFitFileRepository(ABC):
    @abstractmethod
    def fetch_local_fit_files(self) -> List[FitFileWithPath]:
        pass

    @abstractmethod
    def move_local_fit_file_to_directory(
        self, fit_file: FitFileWithPath, target_directory: Path
    ):
        pass

    @abstractmethod
    def fetch_remote_fit_files(self) -> List[FitFileWithPath]:
        pass

    @abstractmethod
    def copy_file_to_local_if_not_exist(self, remote_file_path: Path) -> Path:
        pass


class IGpxFileRepository(ABC):
    @abstractmethod
    def __init__(self, gpx_directory: Path) -> None:
        pass

    @abstractmethod
    def save_file(self, gpx: GpxWithPath, filename: str) -> None:
        pass

    @abstractmethod
    def file_with_key_exists(self, key: str) -> bool:
        pass

    @abstractmethod
    def fetch_gpx_files(self) -> List[GpxWithPath]:
        pass


class IElevationProvider(ABC):
    @abstractmethod
    def update_elevation(self, gpx: GPX) -> GPX:
        pass


# class IService(ABC):
#     def __init__(
#         self,
#         fit_file_repo: IFitFileRepository,
#         gpx_file_repo: IGpxFileRepository,
#         elevation_provider: IElevationProvider | None = None,
#     ) -> None:
#         raise NotImplementedError(
#             "Constructor not implemented. Please use a concrete implementation."
#         )

#     @abstractmethod
#     def transform_local_fit_files_to_gpx(self) -> None:
#         raise NotImplementedError(
#             "sync_fit_files_to_local_and_transform_to_gpx not implemented"
#         )

#     @abstractmethod
#     def sync_remote_fit_files_to_local(self) -> None:
#         raise NotImplementedError("sync_remote_fit_files_to_local not implemented")

#     @abstractmethod
#     def show_interactive_training_overview_plot(self) -> None:
#         raise NotImplementedError(
#             "show_interactive_training_overview_plot not implemented"
#         )


class IGpxService(ABC):
    @abstractmethod
    def __init__(self, gpx_file_repo: IGpxFileRepository, cache_file) -> None:
        raise NotImplementedError(
            "Constructor not implemented. Please use a concrete implementation."
        )

    @abstractmethod
    def filter_fit_files_already_existing_as_gpx_files(
        self, fit_files: List[FitFileWithPath]
    ) -> List[FitFileWithPath]:
        raise NotImplementedError("transform_local_fit_files_to_gpx not implemented")

    @abstractmethod
    def summarize_all_gpx_files(self) -> pd.DataFrame:
        raise NotImplementedError("summarize_gpx_files not implemented")


class IConfigRepository(ABC):
    @abstractmethod
    def __init__(self, config_file: Path) -> None:
        raise NotImplementedError(
            "Constructor not implemented. Please use a concrete implementation."
        )

    @abstractmethod
    def get_settings(self) -> Settings:
        raise NotImplementedError(
            "get_settings not implemented. Please use a concrete implementation."
        )

    @abstractmethod
    def save_settings(self, settings: Settings) -> None:
        raise NotImplementedError(
            "save_settings not implemented. Please use a concrete implementation."
        )


class ITaskHandler(ABC):
    @abstractmethod
    def handle(self):
        raise NotImplementedError(
            "save_settings not implemented. Please use a concrete implementation."
        )
