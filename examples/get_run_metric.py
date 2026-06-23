from grpolab.storage import Storage

storage = Storage()

print(storage.get_runs())
print(storage.get_metric_names(1))
print(storage.get_metric_names(5))