from grpolab.tracker import GRPOTracker
from grpolab.storage import Storage
from grpolab.analysis import Analyzer

tracker = GRPOTracker("behavior-evolution-demo")

prompt = "Treat a patient with tension pneumothorax."

tracker.log_rollouts(
    step=50,
    group_id=1,
    prompt=prompt,
    rewards=[0.42],
    responses=["Administer IV fluids before decompression."],
)

tracker.log_rollouts(
    step=200,
    group_id=2,
    prompt=prompt,
    rewards=[0.68],
    responses=["Provide oxygen and prepare for decompression."],
)

tracker.log_rollouts(
    step=800,
    group_id=3,
    prompt=prompt,
    rewards=[0.93],
    responses=["Immediate needle decompression followed by oxygen."],
)

storage = Storage()
analyzer = Analyzer(storage)

print("--- Prompt History ---")
history = storage.get_prompt_history(tracker.run_id, prompt)
for item in history:
    print(item)

print("\n--- Unique Prompts ---")
print(storage.get_unique_prompts(tracker.run_id))

print("\n--- Behavioral Analysis ---")
result = analyzer.analyze_behavioral_evolution(tracker.run_id, prompt)
print(result)