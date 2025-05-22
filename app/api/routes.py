"""API routes for managing teachers, classes, and students."""

from flask import request, url_for, abort, send_from_directory
from flask_restx import Resource, fields, Namespace, Api
from app.models import Teacher, Class, Student
from app import db
from .spec import api_spec
from sqlalchemy.exc import IntegrityError
import jwt
from datetime import datetime, timedelta
from functools import wraps
import os

# Create API and namespaces
api = Api(title='Striking Vipers API',
         version='1.0',
         description='API for managing teachers, classes, and students in the Striking Vipers educational game')

# Create auth namespace
auth_ns = Namespace('auth', description='Authentication operations')
teacher_ns = Namespace('teachers', description='Teacher operations')
class_ns = Namespace('classes', description='Class operations')
student_ns = Namespace('students', description='Student operations')

# Add namespaces to API
api.add_namespace(auth_ns)
api.add_namespace(teacher_ns)
api.add_namespace(class_ns)
api.add_namespace(student_ns)

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

# Define request/response models for auth namespace
login_input = auth_ns.model('LoginInput', {
    'email': fields.String(required=True, description="User's email"),
    'password': fields.String(required=True, description="User's password")
})

login_response = auth_ns.model('LoginResponse', {
    'token': fields.String(description="JWT token for authentication"),
    'user': fields.Nested(auth_ns.model('UserInfo', {
        'id': fields.Integer(description="User ID"),
        'name': fields.String(description="User's name"),
        'email': fields.String(description="User's email"),
        'role': fields.String(description="User's role (student/teacher)")
    }))
})

signup_input = auth_ns.model('SignupInput', {
    'name': fields.String(required=True, description="User's full name"),
    'email': fields.String(required=True, description="User's email"),
    'password': fields.String(required=True, description="User's password"),
    'role': fields.String(required=True, description="User's role (student/teacher)", enum=['student', 'teacher']),
    'class_code': fields.String(description="Class code (required for students)")
})

signup_response = auth_ns.model('SignupResponse', {
    'id': fields.Integer(description="User ID"),
    'name': fields.String(description="User's name"),
    'email': fields.String(description="User's email"),
    'role': fields.String(description="User's role")
})

# Helper function to add HATEOAS links
def add_links(data, resource_type, resource_id):
    base_url = url_for('api.{}_list'.format(resource_type), _external=True)
    data['links'] = {
        'self': f"{base_url}/{resource_id}",
        'collection': base_url
    }
    return data

def validate_teacher(data):
    """Validate teacher data."""
    if not data.get("name") or not data.get("email") or not data.get("subject"):
        return False, "Name, email and subject are required"
    if "@" not in data.get("email", ""):
        return False, "Invalid email format"
    return True, None

def validate_class(data):
    """Validate class data."""
    if not data.get("id") or not data.get("capacity") or not data.get("teacher_id"):
        return False, "ID, capacity and teacher_id are required"
    if data["capacity"] <= 0:
        return False, "Capacity must be positive"
    teacher = Teacher.query.get(data["teacher_id"])
    if not teacher:
        return False, "Teacher not found"
    return True, None

def validate_student(data):
    """Validate student data."""
    if not data.get("name") or not data.get("email") or not data.get("grade") or not data.get("class_id"):
        return False, "Name, email, grade and class_id are required"
    if "@" not in data.get("email", ""):
        return False, "Invalid email format"
    try:
        grade = int(data["grade"])
        if grade < 1 or grade > 12:
            return False, "Grade must be between 1 and 12"
    except ValueError:
        return False, "Grade must be a number"
    
    classroom = Class.query.get(data["class_id"])
    if not classroom:
        return False, "Class not found"
    
    # Check class capacity
    current_students = Student.query.filter_by(class_id=data["class_id"]).count()
    if current_students >= classroom.capacity:
        return False, "Class is at capacity"
    
    return True, None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return {'message': 'Token is missing'}, 401

        try:
            # Check if token has Bearer prefix
            if not token.startswith('Bearer '):
                return {'message': 'Invalid token format'}, 401
                
            token = token.split(' ')[1]  # Remove 'Bearer ' prefix
            data = jwt.decode(token, 'your-secret-key', algorithms=['HS256'])
            
            current_user = None
            if data['role'] == 'student':
                current_user = Student.query.get(data['user_id'])
            else:
                current_user = Teacher.query.get(data['user_id'])
                
            if not current_user:
                return {'message': 'User not found'}, 401
                
        except jwt.ExpiredSignatureError:
            return {'message': 'Token has expired'}, 401
        except jwt.InvalidTokenError:
            return {'message': 'Token is invalid'}, 401
        except Exception as e:
            return {'message': 'Token validation failed'}, 401

        return f(current_user, *args, **kwargs)
    return decorated

class TeacherList(Resource):
    """Operations for managing teachers."""

    @token_required
    def get(self, current_user):
        """List all teachers."""
        teachers = Teacher.query.all()
        return [{
            "id": t.id,
            "name": t.name,
            "email": t.email,
            "subject": t.subject
        } for t in teachers], 200

    @token_required
    def post(self, current_user):
        """Create a new teacher."""
        data = request.json
        
        # Validate data
        is_valid, error = validate_teacher(data)
        if not is_valid:
            return {"message": error}, 400
            
        try:
            teacher = Teacher(
                name=data["name"],
                email=data["email"],
                subject=data["subject"]
            )
            teacher.set_password("password123")  # Set default password
            db.session.add(teacher)
            db.session.commit()
            return {
                "id": teacher.id,
                "name": teacher.name,
                "email": teacher.email,
                "subject": teacher.subject
            }, 201
        except IntegrityError:
            db.session.rollback()
            return {"message": "Email already exists"}, 400

class TeacherResource(Resource):
    """Operations for managing a specific teacher."""

    @token_required
    def get(self, current_user, teacher_id):
        """Get a specific teacher."""
        teacher = Teacher.query.get_or_404(teacher_id)
        return {
            "id": teacher.id,
            "name": teacher.name,
            "email": teacher.email,
            "subject": teacher.subject
        }, 200

    @token_required
    def put(self, current_user, teacher_id):
        """Update a specific teacher."""
        teacher = Teacher.query.get_or_404(teacher_id)
        data = request.json
        
        # Validate data
        is_valid, error = validate_teacher(data)
        if not is_valid:
            return {"message": error}, 400
            
        try:
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
        except IntegrityError:
            db.session.rollback()
            return {"message": "Email already exists"}, 400

    @token_required
    def delete(self, current_user, teacher_id):
        """Delete a specific teacher."""
        teacher = Teacher.query.get_or_404(teacher_id)
        db.session.delete(teacher)
        db.session.commit()
        return '', 204

class ClassList(Resource):
    """Operations for managing classes."""

    @token_required
    def get(self, current_user):
        """List all classes."""
        classes = Class.query.all()
        return [{
            "id": c.id,
            "capacity": c.capacity,
            "teacher_id": c.teacher_id
        } for c in classes], 200

    @token_required
    def post(self, current_user):
        """Create a new class."""
        data = request.json
        
        # Validate data
        is_valid, error = validate_class(data)
        if not is_valid:
            return {"message": error}, 400
            
        try:
            class_ = Class(
                id=data["id"],
                capacity=data["capacity"],
                teacher_id=data["teacher_id"]
            )
            db.session.add(class_)
            db.session.commit()
            return {
                "id": class_.id,
                "capacity": class_.capacity,
                "teacher_id": class_.teacher_id
            }, 201
        except IntegrityError:
            db.session.rollback()
            return {"message": "Class ID already exists"}, 400

class ClassResource(Resource):
    """Operations for managing a specific class."""

    @token_required
    def get(self, current_user, class_id):
        """Get a specific class."""
        class_ = Class.query.get_or_404(class_id)
        return {
            "id": class_.id,
            "capacity": class_.capacity,
            "teacher_id": class_.teacher_id
        }, 200

    @token_required
    def put(self, current_user, class_id):
        """Update a specific class."""
        class_ = Class.query.get_or_404(class_id)
        data = request.json
        
        # Validate data
        is_valid, error = validate_class(data)
        if not is_valid:
            return {"message": error}, 400
            
        try:
            class_.capacity = data["capacity"]
            class_.teacher_id = data["teacher_id"]
            db.session.commit()
            return {
                "id": class_.id,
                "capacity": class_.capacity,
                "teacher_id": class_.teacher_id
            }, 200
        except IntegrityError:
            db.session.rollback()
            return {"message": "Invalid teacher ID"}, 400

    @token_required
    def delete(self, current_user, class_id):
        """Delete a specific class."""
        class_ = Class.query.get_or_404(class_id)
        db.session.delete(class_)
        db.session.commit()
        return '', 204

class StudentList(Resource):
    """Operations for managing students."""

    @token_required
    def get(self, current_user):
        """List all students."""
        students = Student.query.all()
        return [{
            "id": s.id,
            "name": s.name,
            "email": s.email,
            "grade": s.grade,
            "class_id": s.class_id
        } for s in students], 200

    @token_required
    def post(self, current_user):
        """Create a new student."""
        data = request.json
        
        # Validate data
        is_valid, error = validate_student(data)
        if not is_valid:
            return {"message": error}, 400
            
        try:
            student = Student(
                name=data["name"],
                email=data["email"],
                grade=data["grade"],
                class_id=data["class_id"]
            )
            student.set_password("password123")  # Set default password
            db.session.add(student)
            db.session.commit()
            return {
                "id": student.id,
                "name": student.name,
                "email": student.email,
                "grade": student.grade,
                "class_id": student.class_id
            }, 201
        except IntegrityError:
            db.session.rollback()
            return {"message": "Email already exists"}, 400

class StudentResource(Resource):
    """Operations for managing a specific student."""

    @token_required
    def get(self, current_user, student_id):
        """Get a specific student."""
        student = Student.query.get_or_404(student_id)
        return {
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "grade": student.grade,
            "class_id": student.class_id
        }, 200

    @token_required
    def put(self, current_user, student_id):
        """Update a specific student."""
        student = Student.query.get_or_404(student_id)
        data = request.json
        
        # Validate data
        is_valid, error = validate_student(data)
        if not is_valid:
            return {"message": error}, 400
            
        try:
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
        except IntegrityError:
            db.session.rollback()
            return {"message": "Email already exists"}, 400

    @token_required
    def delete(self, current_user, student_id):
        """Delete a specific student."""
        student = Student.query.get_or_404(student_id)
        db.session.delete(student)
        db.session.commit()
        return '', 204

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.doc('login')
    @auth_ns.expect(login_input)
    @auth_ns.response(200, 'Login successful', login_response)
    @auth_ns.response(401, 'Invalid credentials')
    def post(self):
        """User login endpoint"""
        data = request.json
        email = data.get('email')
        password = data.get('password')

        # Try to find user in both Student and Teacher tables
        user = Student.query.filter_by(email=email).first()
        role = 'student'
        if not user:
            user = Teacher.query.filter_by(email=email).first()
            role = 'teacher'

        if not user or not user.check_password(password):
            return {'message': 'Invalid credentials'}, 401

        # Generate JWT token
        token = jwt.encode({
            'user_id': user.id,
            'role': role,
            'exp': datetime.utcnow() + timedelta(days=1)
        }, 'your-secret-key', algorithm='HS256')

        return {
            'token': token,
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': role
            }
        }

@auth_ns.route('/signup')
class Signup(Resource):
    @auth_ns.doc('signup')
    @auth_ns.expect(signup_input)
    @auth_ns.response(201, 'User created successfully', signup_response)
    @auth_ns.response(400, 'Invalid input')
    def post(self):
        """User signup endpoint"""
        data = request.json
        
        # Validate required fields
        required_fields = ['name', 'email', 'password', 'role']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return {'message': f'Missing required fields: {", ".join(missing_fields)}'}, 400
            
        role = data['role']
    
        if role == 'student':
            # Validate class code for students
            class_code = data.get('class_code')
            if not class_code:
                return {'message': 'Class code is required for students'}, 400
            class_obj = Class.query.get(class_code)
            if not class_obj:
                return {'message': 'Invalid class code'}, 400
    
            # Create student
            try:
                student = Student(
                    name=data['name'],
                    email=data['email'],
                    grade='10',  # Default grade, can be updated later
                    class_id=class_code
                )
                student.set_password(data['password'])
                db.session.add(student)
                db.session.commit()
                return {
                    'id': student.id,
                    'name': student.name,
                    'email': student.email,
                    'role': 'student'
                }, 201
            except IntegrityError:
                db.session.rollback()
                return {'message': 'Email already exists'}, 400
    
        elif role == 'teacher':
            # Create teacher
            try:
                teacher = Teacher(
                    name=data['name'],
                    email=data['email'],
                    subject='General'  # Default subject, can be updated later
                )
                teacher.set_password(data['password'])
                db.session.add(teacher)
                db.session.commit()
                return {
                    'id': teacher.id,
                    'name': teacher.name,
                    'email': teacher.email,
                    'role': 'teacher'
                }, 201
            except IntegrityError:
                db.session.rollback()
                return {'message': 'Email already exists'}, 400
        else:
            return {'message': 'Invalid role'}, 400
