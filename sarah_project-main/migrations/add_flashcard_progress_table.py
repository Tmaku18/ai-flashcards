"""
Migration script to add flashcard_progress table.
"""
import sqlite3
import os

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
    # Check if the flashcard_progress table already exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='flashcard_progress'")
    table_exists = cursor.fetchone()
    
    if not table_exists:
        # Create the flashcard_progress table
        cursor.execute("""
        CREATE TABLE flashcard_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            flashcard_id INTEGER NOT NULL,
            session_id INTEGER,
            is_correct BOOLEAN NOT NULL,
            difficulty TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (flashcard_id) REFERENCES flashcards (id),
            FOREIGN KEY (session_id) REFERENCES study_sessions (id)
        )
        """)
        
        # Create indexes for better performance
        cursor.execute("CREATE INDEX idx_flashcard_progress_user_id ON flashcard_progress (user_id)")
        cursor.execute("CREATE INDEX idx_flashcard_progress_flashcard_id ON flashcard_progress (flashcard_id)")
        cursor.execute("CREATE INDEX idx_flashcard_progress_session_id ON flashcard_progress (session_id)")
        
        # Commit the changes
        conn.commit()
        print("Migration successful: added flashcard_progress table.")
    else:
        print("Table flashcard_progress already exists.")
except Exception as e:
    # Rollback in case of error
    conn.rollback()
    print(f"Migration failed: {str(e)}")
finally:
    # Close the connection
    conn.close()
