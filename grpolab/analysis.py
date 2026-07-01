import statistics
class Analyzer:
    def __init__(self,storage):
        self.storage=storage
    
    def analyze_metric(self,run_id,metric_name):
        data=self.storage.get_metrics(run_id,metric_name)
        if not data:
            return {
                "status": "no_data",
                "metric": metric_name,
                "message": f"No data found for metric '{metric_name}' in run {run_id}."
            }

        best_step=data[0][0]
        best_value=data[0][1]

        for step, value in data:
            if value > best_value:
                best_value = value
                best_step = step

        first_value = data[0][1]
        last_value = data[-1][1]
        if last_value > first_value:
            trend = "Increasing"
        elif last_value < first_value:
            trend = "Decreasing"
        else:
            trend = "Stable"
        return {
            "status": "success",
            "metric": metric_name,
            "summary": {
                "trend": trend
            },
            "statistics": {
                "best_value": best_value,
                "best_step": best_step
            }
        }
    def analyze_rollout_group(self, run_id, group_id):
        rewards = self.storage.get_rollouts(run_id, group_id)

        if not rewards:
            return {
                "status": "no_data",
                "group_id": group_id,
                "message": f"No rollouts found for group {group_id}."
            }

        variance = statistics.pvariance(rewards)

        return {
            "status": "success",
            "group_id": group_id,
            "statistics": {
                "reward_variance": variance,
                "mean_reward": statistics.mean(rewards),
                "max_reward": max(rewards),
                "min_reward": min(rewards),
                "num_rollouts": len(rewards)
            }
        }
    
    def analyze_behavioral_evolution(self, run_id, prompt):
        history = self.storage.get_prompt_history(run_id, prompt)

        if not history:
            return {
                "status": "no_data",
                "prompt": prompt,
                "message": f"No rollout history found for this prompt in run {run_id}.",
            }

        earliest = history[0]
        latest = history[-1]

        reward_change = round(latest["reward"] - earliest["reward"], 4)

        if abs(earliest["reward"]) > 1e-9:
            reward_change_percent = round(
                (reward_change / abs(earliest["reward"])) * 100, 1
            )
        else:
            reward_change_percent = None

        return {
            "status": "success",
            "prompt": prompt,
            "earliest": {
                "step": earliest["step"],
                "reward": round(earliest["reward"], 4),
                "response": earliest["response"],
            },
            "latest": {
                "step": latest["step"],
                "reward": round(latest["reward"], 4),
                "response": latest["response"],
            },
            "learning_summary": {
                "reward_change": reward_change,
                "reward_change_percent": reward_change_percent,
                "improved": reward_change > 0,
                "steps_observed": latest["step"] - earliest["step"],
            },
        }
