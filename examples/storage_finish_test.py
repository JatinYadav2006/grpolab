from grpolab.tracker import GRPOTracker

tracker=GRPOTracker("completion-test")

tracker.log(
    10,
    {
        "reward_mean":0.8
    }
)
tracker.finish()