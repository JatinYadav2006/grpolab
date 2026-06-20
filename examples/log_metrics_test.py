from grpolab.tracker import GRPOTracker
tracker = GRPOTracker("test-run")

tracker.log(
    10,
    {
        "reward_mean":0.8,
        "loss":0.2
    }
)

tracker.log(
    20,
    {
        "reward_mean":0.9,
        "loss":0.15
    }
)