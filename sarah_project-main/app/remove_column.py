"""
Script to remove cards_per_session column from users table
"""
import sqlite3
from app.database import SQLALCHEMY_DATABASE_URL

# Extract the database path from the SQLAlchemy URL
db_path = SQLALCHEMY_DATABASE_URL.replace("sqlite:///", "")

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("Creating a backup of the users table...")
# Create a backup of the users table
cursor.execute("CREATE TABLE users_backup AS SELECT id, username, email, hashed_password, is_active, created_at FROM users")

# Drop the original table
print("Dropping the original users table...")
cursor.execute("DROP TABLE users")

# Create a new users table without the cards_per_session column
print("Creating a new users table without the cards_per_session column...")
cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR UNIQUE,
    email VARCHAR UNIQUE,
    hashed_password VARCHAR,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Copy data from the backup table to the new table
print("Copying data from backup to the new table...")
cursor.execute("""
INSERT INTO users (id, username, email, hashed_password, is_active, created_at)
SELECT id, username, email, hashed_password, is_active, created_at FROM users_backup
""")

# Drop the backup table
print("Dropping the backup table...")
cursor.execute("DROP TABLE users_backup")

# Commit the changes
conn.commit()
print("Column removed successfully!")

# Close the connection
conn.close()
