class GRPOTracker:
    def __init__(self,run_name):
        self.run_name=run_name

    def log(self,step,metrics):
        print(f"Step {step}")
        print(metrics)

    def finish(self):
        print(f"Run {self.run_name} finished.")