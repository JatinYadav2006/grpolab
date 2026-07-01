from grpolab.tracker import GRPOTracker
from grpolab.storage import Storage
from grpolab.analysis import Analyzer

tracker = GRPOTracker("behavior-evolution-demo")
# Log some metrics so the dashboard metric viewer also works
tracker.log(step=50, metrics={"reward_mean": 0.42, "kl_divergence": 0.02})
tracker.log(step=200, metrics={"reward_mean": 0.68, "kl_divergence": 0.03})
tracker.log(step=800, metrics={"reward_mean": 0.93, "kl_divergence": 0.04})
tracker.finish()
prompt = "Treat a patient with tension pneumothorax."

# Step 50 — early training, wrong clinical decision
tracker.log_rollouts(
    step=50,
    group_id=1,
    prompt=prompt,
    rewards=[0.42],
    responses=["Administer IV fluids before decompression."],
)

# Step 200 — mid training, partially correct
tracker.log_rollouts(
    step=200,
    group_id=2,
    prompt=prompt,
    rewards=[0.68],
    responses=["Provide oxygen and prepare for decompression."],
)

# Step 800 — late training, correct clinical decision
tracker.log_rollouts(
    step=800,
    group_id=3,
    prompt=prompt,
    rewards=[0.93],
    responses=["Immediate needle decompression followed by oxygen. Monitor airway and prepare definitive chest tube placement."],
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

print(f"\nRun ID: {tracker.run_id}")
print("Use this run ID in the dashboard to see the behavioral evolution demo.")