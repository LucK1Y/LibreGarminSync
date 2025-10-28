from matplotlib import pyplot as plt
from matplotlib.widgets import Slider
from tqdm import tqdm
from Interfaces import IGpxService, ITaskHandler
from Interfaces import (
    IFitFileRepository,
)
import seaborn


class ShowInteractiveTrainingOverviewPlotHandler(ITaskHandler):
    def __init__(
        self,
        gpx_service: IGpxService,
    ) -> None:
        self.gpx_service = gpx_service

    def handle(self):
        start_df = self.gpx_service.summarize_all_gpx_files()
        rule = "W-MON"
        weekly_df = start_df.resample(rule, on="date").sum()

        window_size_in_weeks = 4
        moving_averages = (
            weekly_df[
                ["total_distance_km", "total_elevation_gain", "total_elevation_loss"]
            ]
            .rolling(window=window_size_in_weeks)
            .mean()
        )
        weekly_df = weekly_df.join(moving_averages, rsuffix="_mv")
        print(weekly_df.columns)

        # seaborn.set_style("whitegrid")
        fig, axes = plt.subplots(2, 1, figsize=(10, 6))

        plt.subplots_adjust(left=0.1, bottom=0.25)
        ax_slider = plt.axes([0.1, 0.1, 0.8, 0.05])
        slider = Slider(
            ax_slider,
            "Weeks Back",
            valmin=2,
            valmax=len(weekly_df),
            valinit=min(len(weekly_df), 10),
            valstep=1,
        )

        def update(val):
            weeks = int(slider.val)
            data_subset = weekly_df.iloc[-weeks:]
            df_height_data = data_subset.reset_index().melt(
                id_vars="date",
                value_vars=[
                    "total_elevation_gain",
                    "total_elevation_loss",
                    "total_elevation_gain_mv",
                    "total_elevation_loss_mv",
                ],
            )
            axes[0].clear()
            axes[1].clear()

            seaborn.lineplot(
                data=data_subset,
                x="date",
                y="total_distance_km",
                ax=axes[0],
                label="Distance (km)",
            )
            seaborn.lineplot(
                data=data_subset,
                x="date",
                y="total_distance_km_mv",
                ax=axes[0],
                color="green",
                label=f"Distance (km): {window_size_in_weeks}-week moving average",
            )
            seaborn.lineplot(
                data=df_height_data, x="date", y="value", ax=axes[1], hue="variable"
            )

            fig.canvas.draw_idle()

        update(slider.val)
        slider.on_changed(update)
        plt.show()
