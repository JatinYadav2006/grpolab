from grpolab.storage import Storage
class GRPOTracker:
    def __init__(self,run_name):
        self.run_name=run_name
        self.storage=Storage()
        self.run_id=self.storage.create_run(run_name)

    def log(self,step,metrics):
        self.storage.log_metrics(self.run_id,step,metrics)
    def log_rollouts(self, step, group_id, rewards,responses):
        self.storage.log_rollouts(
            run_id=self.run_id, 
            step=step, 
            group_id=group_id, 
            rewards=rewards,
            responses=responses,
        )

    def finish(self):
        self.storage.finish_run(self.run_id)
        print(f"Run {self.run_name} finished.")