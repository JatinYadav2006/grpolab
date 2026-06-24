import sqlite3
from datetime import datetime
class Storage:

    def __init__(self,db_path="data/grpolab.db"):
        self.db_path=db_path
        self.create_tables()
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
        conn=sqlite3.connect(self.db_path)
        cursor=conn.cursor() 
        cursor.execute("""
        INSERT INTO runs (run_name,status,start_time) VALUES (?,?,?)
        """,(run_name,"running",datetime.now().isoformat())
        )
        run_id=cursor.lastrowid
        conn.commit()
        conn.close()
        return run_id
    def log_metrics(self,run_id,step,metrics):
        if not metrics:
            return
        conn=sqlite3.connect(self.db_path)
        cursor=conn.cursor()
        for key,value in metrics.items():
            cursor.execute(
                """
                INSERT INTO metrics (run_id,step,key,value) VALUES (?,?,?,?)
                """,(run_id,step,key,value)
            )
        conn.commit()
        conn.close()
    def get_metrics(self,run_id,metric_name):
        conn=sqlite3.connect(self.db_path)
        cursor=conn.cursor()
        cursor.execute(
            """
            SELECT step,value from metrics
            WHERE run_id=? 
            AND key=? 
            ORDER BY step
            """,(run_id,metric_name)
        )
        rows=cursor.fetchall()
        conn.close()
        return rows
    def get_runs(self):
        conn=sqlite3.connect(self.db_path)
        cursor=conn.cursor()
        cursor.execute(
            """
            SELECT run_id, run_name, status
            FROM runs
            ORDER BY start_time DESC
            """
        )
        rows=cursor.fetchall()
        conn.close()
        return rows
    def get_metric_names(self,run_id):
        conn=sqlite3.connect(self.db_path)
        cursor=conn.cursor()
        cursor.execute(
            """
            SELECT DISTINCT key
            FROM metrics
            WHERE run_id = ?
            """,(run_id,)
        )
        rows=cursor.fetchall()
        metric_names= [row[0] for row in rows]
        conn.close()
        return metric_names
    def get_run_details(self,run_id):
        conn=sqlite3.connect(self.db_path)
        cursor=conn.cursor()
        cursor.execute(
            """
            SELECT run_id, run_name, status, start_time, end_time
            FROM runs
            WHERE run_id=?  
            """, (run_id,)
        )
        row=cursor.fetchone()
        conn.close()
        return row
    def finish_run(self,run_id):
        conn=sqlite3.connect(self.db_path)
        cursor=conn.cursor()
        cursor.execute(
            """
            UPDATE runs
            SET status=?, end_time=?
            WHERE run_id=?
            """,("completed",datetime.now().isoformat(),run_id)
        )
        conn.commit()
        conn.close()