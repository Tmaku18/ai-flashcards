"""
Script to add cards_per_session column to users table
"""

import sqlite3
from app.database import SQLALCHEMY_DATABASE_URL

# Extract the database path from the SQLAlchemy URL
db_path = SQLALCHEMY_DATABASE_URL.replace("sqlite:///", "")

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check if the column already exists
cursor.execute("PRAGMA table_info(users)")
columns = cursor.fetchall()
column_names = [column[1] for column in columns]

if "cards_per_session" not in column_names:
    print("Adding cards_per_session column to users table...")
    # Add the new column with a default value of 20
    cursor.execute("ALTER TABLE users ADD COLUMN cards_per_session INTEGER DEFAULT 20")
    conn.commit()
    print("Column added successfully!")
else:
    print("Column cards_per_session already exists.")

# Close the connection
conn.close()
