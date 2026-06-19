import sqlite3

class Storage:

    def __init__(self,db_path="data/grpolab.db"):
        self.db_path=db_path
    def create_tables(self):
        conn=sqlite3.connect(self.db_path)
        cursor=conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS runs(
        run_id INTEGER PRIMARY KEY,
        run_name TEXT,
        status TEXT,
        start_time TEXT,
        end_time TEXT
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS metrics(
        metric_id INTEGER PRIMARY KEY,
        run_id INTEGER,
        step INTEGER,
        key TEXT,
        value REAL,
        FOREIGN KEY(run_id)
        REFERENCES runs(run_id)
        )
        """)
        conn.commit()
        conn.close()
    def create_run(self,run_name):
        pass
    def log_metrics(self,run_id,step,metrics):
        pass
    def finish_run(self,run_id):
        pass