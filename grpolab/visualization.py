from grpolab.storage import Storage
import matplotlib.pyplot as plt

class Visualizer:
    
    def __init__(self):
        self.storage=Storage()
    
    def plot_metric(self, run_id ,metric_name, title=None, xlabel="Training Step", ylabel=None):
        data=self.storage.get_metrics(run_id, metric_name)
        if not data:
            print(f"No data found for metric "
            f"'{metric_name}' in run {run_id}.")
            return
        if title is None:
            title = f"{metric_name} vs Training Step"
        if ylabel is None:
            ylabel = metric_name
        steps,value=map(list,zip(*data))
        plt.plot(steps,value,marker="o")
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.show()