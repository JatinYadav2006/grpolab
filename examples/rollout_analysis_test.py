from grpolab.tracker import GRPOTracker
from grpolab.storage import Storage
from grpolab.analysis import Analyzer

tracker = GRPOTracker("rollout-analysis-test")

tracker.log_rollouts(
    step=1,
    group_id=1,
    rewards=[0.82, 0.75, 0.91]
)

storage = Storage()
analyzer = Analyzer(storage)

result = analyzer.analyze_rollout_group(
    tracker.run_id,
    1
)

print(result)