from tqdm import tqdm
from Interfaces import ITaskHandler
from entities import GpxWithPath
from coords_transformations import semicircle_to_degree
from gpxpy.gpx import GPXTrackPoint
from Interfaces import (
    IGpxFileRepository,
    IFitFileRepository,
    IGpxService,
    IElevationProvider,
)
from typing import Optional


class TransformLocalFitToGpxHandler(ITaskHandler):
    def __init__(
        self,
        fit_file_repo: IFitFileRepository,
        gpx_file_repo: IGpxFileRepository,
        gpx_service: IGpxService,
        elevation_provider: Optional[IElevationProvider] = None,
    ) -> None:
        self.fit_file_repo = fit_file_repo
        self.gpx_file_repo = gpx_file_repo
        self.gpx_service = gpx_service
        self.elevation_provider = elevation_provider

    def handle(self):
        fit_files = self.fit_file_repo.fetch_local_fit_files()
        fit_files = self.gpx_service.filter_fit_files_already_existing_as_gpx_files(
            fit_files
        )

        for fit_file in tqdm(fit_files, desc="Processing FIT files", unit="file"):
            fit_file_key = fit_file.file_path.stem

            sport = fit_file.get_sport()
            if sport and sport != "running":
                print(
                    f"Warning: Sport '{sport}' in FIT file {fit_file.file_path} is not supported. Skipping."
                )
                continue

            gpx_points = []
            for record in fit_file.get_records():
                # fitparse.records.DataMessage

                lat = record.get_value("position_lat")
                lon = record.get_value("position_long")
                ele = record.get_value("enhanced_altitude")
                timestamp = record.get_value("timestamp")
                speed = record.get_value("speed")

                if lat is None or lon is None:
                    # print("No lat/lon in record")
                    continue

                lat = semicircle_to_degree(lat)
                lon = semicircle_to_degree(lon)

                gpx_point = GPXTrackPoint(
                    latitude=lat,
                    longitude=lon,
                    time=timestamp,
                    speed=speed,
                    elevation=ele,
                )
                gpx_points.append(gpx_point)

            if not gpx_points:
                print(
                    f"Warning: No track points found in FIT file {fit_file.file_path}"
                )
                continue

            time_stamp = gpx_points[0].time.date().strftime("%Y-%m-%d")
            gpx_file_name = f"{fit_file_key}_{time_stamp}.gpx"
            gpx_wrapper = GpxWithPath.from_trackpoints(
                track_points=gpx_points,
            )

            if self.elevation_provider:
                gpx_wrapper.gpx = self.elevation_provider.update_elevation(
                    gpx_wrapper.gpx
                )

            self.gpx_file_repo.save_file(gpx_wrapper, gpx_file_name)
