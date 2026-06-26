from grpolab.analysis import Analyzer
from grpolab.storage import Storage
storage=Storage()
analysis=Analyzer(storage)
analysis_status= analysis.analyze_metric(3,"reward_mean")

print(analysis_status)