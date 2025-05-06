"""API routes for managing teachers, classes, and students."""

from flask import request, url_for
from flask_restx import Resource, fields
from app.models import Teacher, Class, Student
from app import db
from .spec import api_spec

# Define models for request/response
teacher_model = {
    "name": fields.String(required=True, description="Teacher name"),
    "email": fields.String(required=True, description="Teacher email"),
    "subject": fields.String(required=True, description="Subject taught"),
}

class_model = {
    "id": fields.String(required=True, description="Class ID"),
    "capacity": fields.Integer(required=True, description="Class capacity"),
    "teacher_id": fields.Integer(required=True, description="Teacher ID"),
}

student_model = {
    "name": fields.String(required=True, description="Student name"),
    "email": fields.String(required=True, description="Student email"),
    "grade": fields.String(required=True, description="Student grade"),
    "class_id": fields.String(required=True, description="Class ID"),
}

# Helper function to add HATEOAS links
def add_links(data, resource_type, resource_id):
    base_url = url_for('api.{}_list'.format(resource_type), _external=True)
    data['links'] = {
        'self': f"{base_url}/{resource_id}",
        'collection': base_url
    }
    return data

class TeacherList(Resource):
    """Operations for managing teachers."""

    def get(self):
        """List all teachers."""
        teachers = Teacher.query.all()
        return [{
            "id": t.id,
            "name": t.name,
            "email": t.email,
            "subject": t.subject
        } for t in teachers], 200

    def post(self):
        """Create a new teacher."""
        data = request.json
        teacher = Teacher(
            name=data["name"],
            email=data["email"],
            subject=data["subject"]
        )
        db.session.add(teacher)
        db.session.commit()
        return {
            "id": teacher.id,
            "name": teacher.name,
            "email": teacher.email,
            "subject": teacher.subject
        }, 201

class TeacherResource(Resource):
    """Operations for managing a specific teacher."""

    def get(self, teacher_id):
        """Get a specific teacher."""
        teacher = Teacher.query.get_or_404(teacher_id)
        return {
            "id": teacher.id,
            "name": teacher.name,
            "email": teacher.email,
            "subject": teacher.subject
        }, 200

    def put(self, teacher_id):
        """Update a specific teacher."""
        teacher = Teacher.query.get_or_404(teacher_id)
        data = request.json
        teacher.name = data["name"]
        teacher.email = data["email"]
        teacher.subject = data["subject"]
        db.session.commit()
        return {
            "id": teacher.id,
            "name": teacher.name,
            "email": teacher.email,
            "subject": teacher.subject
        }, 200

    def delete(self, teacher_id):
        """Delete a specific teacher."""
        teacher = Teacher.query.get_or_404(teacher_id)
        db.session.delete(teacher)
        db.session.commit()
        return '', 204

class ClassList(Resource):
    """Operations for managing classes."""

    def get(self):
        """List all classes."""
        classes = Class.query.all()
        return [{
            "id": c.id,
            "capacity": c.capacity,
            "teacher_id": c.teacher_id
        } for c in classes], 200

    def post(self):
        """Create a new class."""
        data = request.json
        class_obj = Class(
            id=data["id"],
            capacity=data["capacity"],
            teacher_id=data["teacher_id"]
        )
        db.session.add(class_obj)
        db.session.commit()
        return {
            "id": class_obj.id,
            "capacity": class_obj.capacity,
            "teacher_id": class_obj.teacher_id
        }, 201

class ClassResource(Resource):
    """Operations for managing a specific class."""

    def get(self, class_id):
        """Get a specific class."""
        class_obj = Class.query.get_or_404(class_id)
        return {
            "id": class_obj.id,
            "capacity": class_obj.capacity,
            "teacher_id": class_obj.teacher_id
        }, 200

    def put(self, class_id):
        """Update a specific class."""
        class_obj = Class.query.get_or_404(class_id)
        data = request.json
        class_obj.capacity = data["capacity"]
        class_obj.teacher_id = data["teacher_id"]
        db.session.commit()
        return {
            "id": class_obj.id,
            "capacity": class_obj.capacity,
            "teacher_id": class_obj.teacher_id
        }, 200

    def delete(self, class_id):
        """Delete a specific class."""
        class_obj = Class.query.get_or_404(class_id)
        db.session.delete(class_obj)
        db.session.commit()
        return '', 204

class StudentList(Resource):
    """Operations for managing students."""

    def get(self):
        """List all students."""
        students = Student.query.all()
        return [{
            "id": s.id,
            "name": s.name,
            "email": s.email,
            "grade": s.grade,
            "class_id": s.class_id
        } for s in students], 200

    def post(self):
        """Create a new student."""
        data = request.json
        student = Student(
            name=data["name"],
            email=data["email"],
            grade=data["grade"],
            class_id=data["class_id"]
        )
        db.session.add(student)
        db.session.commit()
        return {
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "grade": student.grade,
            "class_id": student.class_id
        }, 201

class StudentResource(Resource):
    """Operations for managing a specific student."""

    def get(self, student_id):
        """Get a specific student."""
        student = Student.query.get_or_404(student_id)
        return {
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "grade": student.grade,
            "class_id": student.class_id
        }, 200

    def put(self, student_id):
        """Update a specific student."""
        student = Student.query.get_or_404(student_id)
        data = request.json
        student.name = data["name"]
        student.email = data["email"]
        student.grade = data["grade"]
        student.class_id = data["class_id"]
        db.session.commit()
        return {
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "grade": student.grade,
            "class_id": student.class_id
        }, 200

    def delete(self, student_id):
        """Delete a specific student."""
        student = Student.query.get_or_404(student_id)
        db.session.delete(student)
        db.session.commit()
        return '', 204
