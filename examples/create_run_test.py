from grpolab.storage import Storage

storage=Storage()
storage.create_tables()

run_id=storage.create_run("pulse-er-v1")
print(f"Run ID : {run_id}")
