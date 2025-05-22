"""Database models for the application."""

from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class Teacher(db.Model):
    """Teacher model for storing teacher information."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    classes = db.relationship('Class', backref='teacher', lazy=True)

    def set_password(self, password):
        """Set the password hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the password is correct."""
        return check_password_hash(self.password_hash, password)


class Class(db.Model):
    """Class model for storing class information."""
    id = db.Column(db.String(10), primary_key=True)
    capacity = db.Column(db.Integer, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), 
                         nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    students = db.relationship('Student', backref='class_ref', lazy=True)


class Student(db.Model):
    """Student model for storing student information."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    grade = db.Column(db.String(2), nullable=False)
    class_id = db.Column(db.String(10), db.ForeignKey('class.id'), 
                        nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        """Set the password hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the password is correct."""
        return check_password_hash(self.password_hash, password)
