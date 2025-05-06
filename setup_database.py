import sqlite3
import os

def setup_database():
    # Remove existing database if it exists
    if os.path.exists('game.db'):
        os.remove('game.db')
    
    # Create new database connection
    conn = sqlite3.connect('game.db')
    cursor = conn.cursor()
    
    # Create Students table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Students (
        StudentID INTEGER PRIMARY KEY AUTOINCREMENT,
        StudentFirstName TEXT NOT NULL,
        StudentLastName TEXT NOT NULL,
        StudentUserName TEXT NOT NULL UNIQUE,
        StudentPassWord TEXT NOT NULL,
        ClassCode TEXT NOT NULL
    )
    ''')
    
    # Sample student credentials
    students = [
        ('John', 'Smith', 'john123', 'pass123', 'CLASS1'),
        ('Emma', 'Johnson', 'emma123', 'pass456', 'CLASS2'),
        ('Michael', 'Brown', 'mike123', 'pass789', 'CLASS3'),
        ('Sarah', 'Davis', 'sarah123', 'pass321', 'CLASS1'),
        ('David', 'Wilson', 'david123', 'pass654', 'CLASS2')
    ]
    
    # Insert student data
    cursor.executemany('''
    INSERT INTO Students (StudentFirstName, StudentLastName, StudentUserName, StudentPassWord, ClassCode)
    VALUES (?, ?, ?, ?, ?)
    ''', students)
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print("Database created successfully!")
    print("\nAvailable login credentials:")
    print("----------------------------------------")
    for student in students:
        print(f"Username: {student[2]}")
        print(f"Password: {student[3]}")
        print(f"Class Code: {student[4]}")
        print("----------------------------------------")

if __name__ == "__main__":
    setup_database() 