from configparser import ConfigParser
from dataclasses import dataclass, field
from typing import Generator, List, Optional
from fitparse import FitFile, DataMessage
from pathlib import Path
from enum import Enum
import gpxpy
import gpxpy.gpx


@dataclass
class FitFileWithPath:
    file_path: Path
    _fitfile: Optional[FitFile] = None

    @property
    def fitfile(self) -> FitFile:
        if self._fitfile:
            return self._fitfile

        self._fitfile = FitFile(str(self.file_path))
        return self._fitfile

    def get_records(self) -> Generator[DataMessage, None, None]:
        return self.fitfile.get_messages("record")

    def get_sport(self) -> str:
        sessions = list(self.fitfile.get_messages("session"))
        assert len(sessions) == 1, "Expected exactly one session in the FIT file."

        return sessions[0].get_value("sport")


@dataclass
class GpxStats:
    total_distance_km: float
    total_elevation_gain: float
    total_elevation_loss: float
    total_minutes: int
    date: str
    filename: str


class GpxWithPath:
    def __init__(
        self, file_path: Optional[Path] = None, gpx: Optional[gpxpy.gpx.GPX] = None
    ) -> None:
        if file_path and file_path.exists():
            self._file_path = file_path.resolve()
        self._gpx: Optional[gpxpy.gpx.GPX] = gpx

        if not gpx and not file_path:
            raise ValueError("Either 'gpx' or 'file_path' must be provided.")

    @property
    def gpx(self) -> gpxpy.gpx.GPX:
        if self._gpx is None:
            with self.file_path.open("r") as gpx_file:
                self._gpx = gpxpy.parse(gpx_file)
        return self._gpx

    @property
    def file_path(self) -> Path:
        if not hasattr(self, "_file_path"):
            raise ValueError("File path is not set. Please provide a valid file path.")

        return self._file_path

    @gpx.setter
    def gpx(self, value: gpxpy.gpx.GPX) -> None:
        self._gpx = value

    def get_statistics(self) -> GpxStats:
        total_distance_m = 0.0
        total_elevation_gain = 0.0
        total_elevation_loss = 0.0

        total_minutes = 0

        for track in self.gpx.tracks:
            for segment in track.segments:
                total_distance_m += segment.length_2d() or 0.0

                elevation_data = segment.get_uphill_downhill()
                total_elevation_gain += elevation_data[0] or 0.0
                total_elevation_loss += elevation_data[1] or 0.0

            bounds = track.get_time_bounds()
            if bounds[0] and bounds[1]:
                total_minutes += round((bounds[1] - bounds[0]).total_seconds() / 60.0)

        total_distance_km = total_distance_m / 1000

        return GpxStats(
            total_distance_km=total_distance_km,
            total_elevation_gain=total_elevation_gain,
            total_elevation_loss=total_elevation_loss,
            date=self._file_path.stem.split("_")[1],
            filename=self._file_path.name,
            total_minutes=total_minutes,
        )

    @classmethod
    def from_trackpoints(
        cls, track_points: List[gpxpy.gpx.GPXTrackPoint]
    ) -> "GpxWithPath":
        gpx = gpxpy.gpx.GPX()
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx.tracks.append(gpx_track)
        gpx_track.segments.append(gpx_segment)
        gpx_segment.points += track_points

        return cls(gpx=gpx)


@dataclass
class Settings:
    remote_fit_directory: Path
    local_fit_directory: Path
    gpx_directory: Path
    summary_cache_file: Path
    empty_files_directory: Optional[Path] = None

    @classmethod
    def from_config(cls, config: ConfigParser) -> "Settings":
        empty_files_directory: Optional[Path] = None
        if "empty_files_directory" in config["Paths"].keys():
            empty_files_directory = Path(config["Paths"]["empty_files_directory"])

        return cls(
            remote_fit_directory=Path(
                config["Paths"]["remote_fit_directory"]
            ).resolve(),
            local_fit_directory=Path(config["Paths"]["local_fit_directory"]).resolve(),
            gpx_directory=Path(config["Paths"]["gpx_directory"]).resolve(),
            summary_cache_file=Path(config["Paths"]["summary_cache_file"]).resolve(),
            empty_files_directory=(
                empty_files_directory if empty_files_directory else None
            ),
        )


class Task(Enum):
    TRANSFORM_LOCAL_FIT_TO_GPX = 0
    SYNC_REMOTE_FIT_TO_LOCAL = 1
    Overview_TRAINING = 2


@dataclass
class ConsoleArguments:
    config_file: Path
    tasks: List[Task] = field(default_factory=list)
