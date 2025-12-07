from psycopg import connect
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Use Session Pooler for IPv4 compatibility
# Connection string from Supabase dashboard > Pooler settings
# Using individual parameters to ensure correct parsing
cnxn = connect(
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT', 5432)),
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    sslmode=os.getenv('DB_SSLMODE', 'require')
)

cursor = cnxn.cursor()

query = "SELECT * FROM students"

# # Read SQL query from file
# sql_file = Path(__file__).parent / 'resource' / 'select_sutudents.sql'
# with open(sql_file, 'r', encoding='utf-8') as f:
#     query = f.read().strip()

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)