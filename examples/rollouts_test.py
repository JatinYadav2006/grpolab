from grpolab.tracker import GRPOTracker
from grpolab.storage import Storage

tracker = GRPOTracker("response-storage-demo")

tracker.log_rollouts(
    step=1,
    group_id=1,
    rewards=[
        0.82,
        0.75,
        0.91,
    ],
    responses=[
        "Perform decompression first.",
        "Administer IV fluids.",
        "Immediate needle decompression followed by oxygen.",
    ],
)

storage = Storage()

print(
    storage.get_rollouts(
        tracker.run_id,
        1,
    )
)