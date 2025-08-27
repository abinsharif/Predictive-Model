#!/usr/bin/env python3
import sqlite3
import os
from datetime import datetime

def init_database(db_path='comprehensive_analysis.db'):
    """Initialize the database with schema and sample data"""
    print(f"📊 Initializing database: {db_path}")

    conn = sqlite3.connect(db_path)

    try:
        # Read and execute schema
        with open('data/database_schema.sql', 'r', encoding='utf-8') as f:
            schema = f.read()

        conn.executescript(schema)
        conn.commit()
        print("✅ Database initialized successfully!")
        return True

    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

    finally:
        conn.close()

if __name__ == '__main__':
    init_database()
