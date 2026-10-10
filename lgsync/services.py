from pathlib import Path
from typing import List
import pandas as pd
from entities import FitFileWithPath

from Interfaces import (
    IGpxFileRepository,
    IGpxService,
)

from tqdm import tqdm


class GpxService(IGpxService):
    def __init__(self, gpx_file_repo: IGpxFileRepository, cache_file: Path) -> None:
        self.gpx_file_repo = gpx_file_repo
        self.cache_file = cache_file

    def filter_fit_files_already_existing_as_gpx_files(
        self, fit_files: List[FitFileWithPath]
    ) -> List[FitFileWithPath]:
        gpx_files = self.gpx_file_repo.fetch_gpx_files()
        not_existing_fit_files = fit_files.copy()

        for fit_file in fit_files:
            for gpx_file in gpx_files:
                if fit_file.file_path.stem in gpx_file.file_path.stem:
                    not_existing_fit_files.remove(fit_file)
                    break

        return not_existing_fit_files

    def summarize_all_gpx_files(self) -> pd.DataFrame:
        gpx_files = self.gpx_file_repo.fetch_gpx_files()

        if self.cache_file.exists():
            df_cache = pd.read_csv(self.cache_file)
            df_cache["date"] = pd.to_datetime(df_cache["date"])
            print(f"Found {len(df_cache)} cached files.")

        else:
            print("No stats cache found.")
            df_cache = pd.DataFrame(columns=["filename"])

        cached_file_names = df_cache["filename"].values

        statistics = []
        for gpx_file in tqdm(gpx_files, desc="Processing GPX files", unit="file"):
            if len(df_cache) and gpx_file.file_path.name in cached_file_names:
                continue

            statistics.append(gpx_file.get_statistics())

        df_new = pd.DataFrame(statistics)
        if df_new.empty:
            print("No new GPX files to process.")
            return df_cache

        df = pd.concat([df_cache, df_new])
        df["date"] = pd.to_datetime(df["date"])

        df.to_csv(self.cache_file, index=False)
        print(f"Stats cache written to {self.cache_file}")

        return df
