import sqlite3
import os

# Path to the database
db_path = os.path.join(os.path.dirname(__file__), 'instance', 'scopira.db')

# Check if instance folder exists, if not check root or backend
if not os.path.exists(db_path):
    db_path = os.path.join(os.path.dirname(__file__), 'backend', 'instance', 'scopira.db')

if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
    # Try to find it
    for root, dirs, files in os.walk('.'):
        if 'scopira.db' in files:
            db_path = os.path.join(root, 'scopira.db')
            print(f"Found database at {db_path}")
            break

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN profile_picture VARCHAR(255)")
        conn.commit()
        print("Successfully added profile_picture column to users table.")
    except sqlite3.OperationalError as e:
        print(f"Column might already exist or error: {e}")
    finally:
        conn.close()
else:
    print("Could not find database file.")
