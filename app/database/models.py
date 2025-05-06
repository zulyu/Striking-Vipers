from app import db


class Teacher(db.Model):
    __tablename__ = "Teachers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    subject = db.Column(db.String(255), nullable=False)
    classes = db.relationship("Class", backref="teacher", lazy=True)


class Class(db.Model):
    __tablename__ = "Classes"
    id = db.Column(db.String(255), primary_key=True)
    capacity = db.Column(db.Integer, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("Teachers.id"), nullable=False)
    students = db.relationship("Student", backref="class", lazy=True)


class Student(db.Model):
    __tablename__ = "Students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    grade = db.Column(db.String(255), nullable=False)
    class_id = db.Column(db.String(255), db.ForeignKey("Classes.id"), nullable=False)
