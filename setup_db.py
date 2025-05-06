import mysql.connector
from mysql.connector import Error

def create_database():
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='CPSC498'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database
            cursor.execute("CREATE DATABASE IF NOT EXISTS StrikingVipers")
            print("Database created successfully")
            
            # Switch to the database
            cursor.execute("USE StrikingVipers")
            
            # Create tables
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Teachers (
                    TeacherID INT AUTO_INCREMENT PRIMARY KEY,
                    TeacherFirstName VARCHAR(255) NOT NULL,
                    TeacherLastName VARCHAR(255) NOT NULL,
                    TeacherUserName VARCHAR(255) NOT NULL UNIQUE
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Classes (
                    ClassCode VARCHAR(255) PRIMARY KEY,
                    ClassGrade INT NOT NULL,
                    TeacherID INT NOT NULL,
                    FOREIGN KEY (TeacherID) REFERENCES Teachers(TeacherID)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Students (
                    StudentID INT AUTO_INCREMENT PRIMARY KEY,
                    StudentFirstName VARCHAR(255) NOT NULL,
                    StudentLastName VARCHAR(255) NOT NULL,
                    StudentUserName VARCHAR(255) NOT NULL UNIQUE,
                    ClassCode VARCHAR(255) NOT NULL,
                    FOREIGN KEY (ClassCode) REFERENCES Classes(ClassCode)
                )
            """)
            
            print("Tables created successfully")
            
            # Insert sample data
            cursor.execute("""
                INSERT IGNORE INTO Teachers 
                (TeacherFirstName, TeacherLastName, TeacherUserName)
                VALUES ('John', 'Doe', 'jdoe')
            """)
            
            cursor.execute("""
                INSERT IGNORE INTO Classes 
                (ClassCode, ClassGrade, TeacherID)
                VALUES ('CS101', 10, 1)
            """)
            
            cursor.execute("""
                INSERT IGNORE INTO Students 
                (StudentFirstName, StudentLastName, StudentUserName, ClassCode)
                VALUES ('Jane', 'Smith', 'jsmith', 'CS101')
            """)
            
            connection.commit()
            print("Sample data inserted successfully")
            
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    create_database() 