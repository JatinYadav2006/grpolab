from grpolab.storage import Storage
import matplotlib.pyplot as plt


class Visualizer:

    def __init__(self):
        self.storage = Storage()

    def plot_metric(
        self,
        run_id,
        metric_name,
        title=None,
        xlabel="Training Step",
        ylabel=None,
    ):
        data = self.storage.get_metrics(run_id, metric_name)
        if not data:
            print(
                f"No data found for metric "
                f"'{metric_name}' in run {run_id}."
            )
            return None

        if title is None:
            title = f"{metric_name} vs Training Step"
        if ylabel is None:
            ylabel = metric_name

        steps, values = map(list, zip(*data))
        fig, ax = plt.subplots()
        ax.plot(steps, values, marker="o")
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(True)
        fig.tight_layout()
        return fig
