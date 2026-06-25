import matplotlib.pyplot as plt

from grpolab.visualization import Visualizer

viz = Visualizer()
fig = viz.plot_metric(3, "reward_mean")

if fig is not None:
    plt.show()
