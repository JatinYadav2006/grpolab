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
