from tqdm import tqdm
from Interfaces import ITaskHandler
from Interfaces import (
    IFitFileRepository,
)


class SyncRemoteFitFilesToLocalHandler(ITaskHandler):
    def __init__(
        self,
        fit_file_repo: IFitFileRepository,
    ) -> None:
        self.fit_file_repo = fit_file_repo

    def handle(self):
        remote_fit_files = self.fit_file_repo.fetch_remote_fit_files()
        local_fit_files_names_set = {
            file.file_path.name for file in self.fit_file_repo.fetch_local_fit_files()
        }

        remote_fit_files_to_sync = []
        for remote_fit_file in remote_fit_files:
            if remote_fit_file.file_path.name in local_fit_files_names_set:
                continue
            remote_fit_files_to_sync.append(remote_fit_file)

        for remote_fit_file in tqdm(
            remote_fit_files_to_sync, desc="Copying FIT files", unit="file"
        ):
            self.fit_file_repo.copy_file_to_local_if_not_exist(
                remote_fit_file.file_path
            )
