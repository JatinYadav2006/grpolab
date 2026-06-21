from grpolab.tracker import GRPOTracker

tracker=GRPOTracker("test")

tracker.log(
    10,
    {"reward_mean": 0.8}
)

tracker.log(
    20,
    {"reward_mean": 0.9}
)

data = tracker.storage.get_metrics(
    tracker.run_id,
    "reward_mean"
)

print(data)