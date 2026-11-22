import sqlite3,json
from pathlib import Path
DB=Path(__file__).resolve().parents[2]/"research_history.db"
def init_db():
    with sqlite3.connect(DB) as c:
        c.execute("""CREATE TABLE IF NOT EXISTS runs(
          id TEXT PRIMARY KEY, topic TEXT, status TEXT, stage TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP,
          data TEXT DEFAULT '{}')""")
def save_run(rid,topic):
    init_db()
    with sqlite3.connect(DB) as c:c.execute("INSERT INTO runs(id,topic,status,stage,data) VALUES(?,?,?,?,?)",(rid,topic,"queued","Queued","{}"))
def update_run(rid,**fields):
    with sqlite3.connect(DB) as c:
        row=c.execute("SELECT data FROM runs WHERE id=?",(rid,)).fetchone()
        if not row:return
        data=json.loads(row[0]); data.update({k:v for k,v in fields.items() if k not in ("status","stage")})
        c.execute("UPDATE runs SET status=?,stage=?,data=? WHERE id=?",
                  (fields.get("status",None) or c.execute("SELECT status FROM runs WHERE id=?",(rid,)).fetchone()[0],
                   fields.get("stage",None) or c.execute("SELECT stage FROM runs WHERE id=?",(rid,)).fetchone()[0],
                   json.dumps(data,ensure_ascii=False),rid))
def fetch_run(rid):
    with sqlite3.connect(DB) as c:
        c.row_factory=sqlite3.Row; row=c.execute("SELECT * FROM runs WHERE id=?",(rid,)).fetchone()
    if not row:return None
    result=dict(row); result.update(json.loads(result.pop("data")));return result
def fetch_history():
    with sqlite3.connect(DB) as c:
        c.row_factory=sqlite3.Row; rows=c.execute("SELECT id,topic,status,stage,created_at FROM runs ORDER BY created_at DESC LIMIT 50").fetchall()
    return [dict(r) for r in rows]
