from configProvider import IniFileConfigProvider
from cli import parse_args
from services import GpxService
from repositories import FitFileRepository, GpxFileRepository, SRMTElevationProvider
from tasks.task_factory import TaskFactory


def main():
    console_args = parse_args()

    config_repo = IniFileConfigProvider(console_args.config_file)
    settings = config_repo.get_settings()

    fit_file_repo = FitFileRepository(
        local_fit_directory=settings.local_fit_directory,
        remote_fit_directory=settings.remote_fit_directory,
    )
    gpx_file_repo = GpxFileRepository(settings.gpx_directory)

    gpx_service = GpxService(gpx_file_repo, settings.summary_cache_file)

    elevation_provider = SRMTElevationProvider()

    task_factory: TaskFactory = TaskFactory(console_args.tasks)
    task_factory.run_tasks(
        fit_file_repo=fit_file_repo,
        gpx_file_repo=gpx_file_repo,
        gpx_service=gpx_service,
        elevation_provider=elevation_provider,
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred.\n{e}")
        exit(1)
