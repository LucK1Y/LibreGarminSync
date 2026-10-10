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
        fig, axes = plt.subplots(3, 1, figsize=(15, 10))

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

        # add an actual table for yearly summary into pyplot
        yearly_df = (
            start_df[
                [
                    "total_distance_km",
                    "total_elevation_gain",
                    "total_elevation_loss",
                    "date",
                ]
            ]
            .resample("Y", on="date")
            .sum()
        )

        table_data = yearly_df[
            ["total_distance_km", "total_elevation_gain", "total_elevation_loss"]
        ].round(1)
        table_data.index = table_data.index.year
        table_ax = fig.add_subplot(111, frame_on=False)
        table_ax.xaxis.set_visible(False)
        table_ax.yaxis.set_visible(False)
        table = table_ax.table(
            cellText=table_data.values,
            rowLabels=table_data.index,
            colLabels=table_data.columns,
            cellLoc="center",
            rowLoc="center",
            loc="bottom",
        )
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.5)

        plt.show()
