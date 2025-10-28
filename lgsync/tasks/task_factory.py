from entities import Task
from tasks.transform_local_fit_to_gpx_handler import TransformLocalFitToGpxHandler
from Interfaces import (
    IFitFileRepository,
    IGpxFileRepository,
    IGpxService,
    IElevationProvider,
    ITaskHandler,
)
from typing import List, Optional

from tasks.sync_remote_fit_files_to_local_handler import (
    SyncRemoteFitFilesToLocalHandler,
)
from tasks.show_interactive_training_overview_plot_handler import (
    ShowInteractiveTrainingOverviewPlotHandler,
)


class TaskFactory(object):
    def __init__(self, tasks: List[Task]):
        self.tasks = tasks

    def run_tasks(
        self,
        fit_file_repo: IFitFileRepository,
        gpx_file_repo: IGpxFileRepository,
        gpx_service: IGpxService,
        elevation_provider: Optional[IElevationProvider] = None,
    ):
        self.fit_file_repo = fit_file_repo
        self.gpx_file_repo = gpx_file_repo
        self.gpx_service = gpx_service
        self.elevation_provider = elevation_provider

        for task in self.tasks:
            print(f"**** Running task: {task.name}")
            handler = self.__create_task(task_type=task)

            handler.handle()

    def __create_task(self, task_type: Task) -> ITaskHandler:
        match task_type:
            case Task.TRANSFORM_LOCAL_FIT_TO_GPX:
                return TransformLocalFitToGpxHandler(
                    fit_file_repo=self.fit_file_repo,
                    gpx_file_repo=self.gpx_file_repo,
                    gpx_service=self.gpx_service,
                    elevation_provider=self.elevation_provider,
                )
            case Task.SYNC_REMOTE_FIT_TO_LOCAL:
                return SyncRemoteFitFilesToLocalHandler(
                    fit_file_repo=self.fit_file_repo
                )
            case Task.Overview_TRAINING:
                return ShowInteractiveTrainingOverviewPlotHandler(
                    gpx_service=self.gpx_service
                )
            case _:
                raise ValueError(f"Unknown task type: {task_type}")
