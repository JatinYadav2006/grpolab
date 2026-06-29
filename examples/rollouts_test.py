from grpolab.tracker import GRPOTracker

tracker = GRPOTracker("rollout-test-run")

tracker.log_rollouts(
    step=100,
    group_id=1,
    rewards=[0.82, 0.75, 0.91]
)

rollouts = tracker.storage.get_rollouts(run_id=tracker.run_id, group_id=1)
print(rollouts)