import sqlite3
import pandas as pd

# Connect to your SQLite database
conn = sqlite3.connect("../data/disaster.db")

# Load the disasters table into a DataFrame
df = pd.read_sql_query("SELECT * FROM disasters", conn)

# Export to CSV
df.to_csv("disasters_export.csv", index=False)

conn.close()
print("✅ Exported to disasters_export.csv")
