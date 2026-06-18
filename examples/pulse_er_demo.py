from grpolab.tracker import GRPOTracker

tracker = GRPOTracker("pulse-er-v1")
tracker.log(10,{'reward_mean':10,'loss':0.9})
tracker.log(20,{'reward_mean':8,'loss':2.4})

tracker.finish()