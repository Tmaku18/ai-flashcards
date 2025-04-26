"""
Migration script to add updated_at column to flashcard_sets table.
"""
import sqlite3
import os
from datetime import datetime

# Get the database file path
db_path = "flashcard_app.db"

# Check if the database file exists
if not os.path.exists(db_path):
    print(f"Database file {db_path} not found.")
    exit(1)

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Check if the updated_at column already exists
    cursor.execute("PRAGMA table_info(flashcard_sets)")
    columns = cursor.fetchall()
    column_names = [column[1] for column in columns]
    
    if "updated_at" not in column_names:
        # Add the updated_at column
        cursor.execute("ALTER TABLE flashcard_sets ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        
        # Update existing rows to set updated_at to the same value as created_at
        cursor.execute("UPDATE flashcard_sets SET updated_at = created_at")
        
        # Commit the changes
        conn.commit()
        print("Migration successful: added updated_at column to flashcard_sets table.")
    else:
        print("Column updated_at already exists in flashcard_sets table.")
except Exception as e:
    # Rollback in case of error
    conn.rollback()
    print(f"Migration failed: {str(e)}")
finally:
    # Close the connection
    conn.close()
