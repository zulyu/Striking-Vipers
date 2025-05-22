from app import create_app, db
from app.models import Teacher, Class, Student

def init_db():
    app = create_app('development')
    with app.app_context():
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()
        
        # Add sample data
        teacher = Teacher(
            name='John Doe',
            email='jdoe@example.com',
            subject='Computer Science'
        )
        db.session.add(teacher)
        db.session.commit()
        
        # Add a sample class
        classroom = Class(
            id='CS101',
            capacity=30,
            teacher_id=teacher.id
        )
        db.session.add(classroom)
        db.session.commit()
        
        # Add a sample student
        student = Student(
            name='Jane Smith',
            email='jsmith@example.com',
            grade='10',
            class_id=classroom.id
        )
        db.session.add(student)
        db.session.commit()
        
        print("Database recreated and sample data added successfully!")

if __name__ == '__main__':
    init_db() 