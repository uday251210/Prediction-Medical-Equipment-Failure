import sqlite3
conn = sqlite3.connect("database/equipment.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT,
    device_type TEXT,
    age REAL,
    maintenance_cost REAL,
    downtime REAL,
    maintenance_frequency REAL,
    manufacturer TEXT,
    country TEXT,
    maintenance_class TEXT,
    prediction TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)''')
conn.commit()
conn.close()
print("Database initialized at database/equipment.db")