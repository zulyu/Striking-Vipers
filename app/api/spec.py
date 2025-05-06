from flask_restx import fields

# Define the API specification
api_spec = {
    "openapi": "3.0.0",
    "info": {
        "title": "Striking Vipers API",
        "version": "1.0",
        "description": "API for managing teachers, classes, and students in the Striking Vipers educational game"
    },
    "servers": [
        {
            "url": "/",
            "description": "Base URL"
        }
    ],
    "paths": {
        "/teachers": {
            "get": {
                "summary": "List all teachers",
                "description": "Returns a list of all teachers",
                "responses": {
                    "200": {
                        "description": "Successful operation",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/components/schemas/Teacher"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "post": {
                "summary": "Create a new teacher",
                "description": "Creates a new teacher",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/Teacher"
                            }
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Teacher created successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Teacher"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/teachers/{teacher_id}": {
            "get": {
                "summary": "Get a specific teacher",
                "description": "Returns a specific teacher by ID",
                "parameters": [
                    {
                        "name": "teacher_id",
                        "in": "path",
                        "required": True,
                        "schema": {
                            "type": "integer"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful operation",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Teacher"
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Teacher not found"
                    }
                }
            },
            "put": {
                "summary": "Update a specific teacher",
                "description": "Updates a specific teacher by ID",
                "parameters": [
                    {
                        "name": "teacher_id",
                        "in": "path",
                        "required": True,
                        "schema": {
                            "type": "integer"
                        }
                    }
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/Teacher"
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Teacher updated successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Teacher"
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Teacher not found"
                    }
                }
            },
            "delete": {
                "summary": "Delete a specific teacher",
                "description": "Deletes a specific teacher by ID",
                "parameters": [
                    {
                        "name": "teacher_id",
                        "in": "path",
                        "required": True,
                        "schema": {
                            "type": "integer"
                        }
                    }
                ],
                "responses": {
                    "204": {
                        "description": "Teacher deleted successfully"
                    },
                    "404": {
                        "description": "Teacher not found"
                    }
                }
            }
        },
        "/classes": {
            "get": {
                "summary": "List all classes",
                "description": "Returns a list of all classes",
                "responses": {
                    "200": {
                        "description": "Successful operation",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/components/schemas/Class"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "post": {
                "summary": "Create a new class",
                "description": "Creates a new class",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/Class"
                            }
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Class created successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Class"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/classes/{class_id}": {
            "get": {
                "summary": "Get a specific class",
                "description": "Returns a specific class by ID",
                "parameters": [
                    {
                        "name": "class_id",
                        "in": "path",
                        "required": True,
                        "schema": {
                            "type": "string"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful operation",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Class"
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Class not found"
                    }
                }
            },
            "put": {
                "summary": "Update a specific class",
                "description": "Updates a specific class by ID",
                "parameters": [
                    {
                        "name": "class_id",
                        "in": "path",
                        "required": True,
                        "schema": {
                            "type": "string"
                        }
                    }
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/Class"
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Class updated successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Class"
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Class not found"
                    }
                }
            },
            "delete": {
                "summary": "Delete a specific class",
                "description": "Deletes a specific class by ID",
                "parameters": [
                    {
                        "name": "class_id",
                        "in": "path",
                        "required": True,
                        "schema": {
                            "type": "string"
                        }
                    }
                ],
                "responses": {
                    "204": {
                        "description": "Class deleted successfully"
                    },
                    "404": {
                        "description": "Class not found"
                    }
                }
            }
        },
        "/students": {
            "get": {
                "summary": "List all students",
                "description": "Returns a list of all students",
                "responses": {
                    "200": {
                        "description": "Successful operation",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/components/schemas/Student"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "post": {
                "summary": "Create a new student",
                "description": "Creates a new student",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/Student"
                            }
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Student created successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Student"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/students/{student_id}": {
            "get": {
                "summary": "Get a specific student",
                "description": "Returns a specific student by ID",
                "parameters": [
                    {
                        "name": "student_id",
                        "in": "path",
                        "required": True,
                        "schema": {
                            "type": "integer"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful operation",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Student"
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Student not found"
                    }
                }
            },
            "put": {
                "summary": "Update a specific student",
                "description": "Updates a specific student by ID",
                "parameters": [
                    {
                        "name": "student_id",
                        "in": "path",
                        "required": True,
                        "schema": {
                            "type": "integer"
                        }
                    }
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/Student"
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Student updated successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Student"
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Student not found"
                    }
                }
            },
            "delete": {
                "summary": "Delete a specific student",
                "description": "Deletes a specific student by ID",
                "parameters": [
                    {
                        "name": "student_id",
                        "in": "path",
                        "required": True,
                        "schema": {
                            "type": "integer"
                        }
                    }
                ],
                "responses": {
                    "204": {
                        "description": "Student deleted successfully"
                    },
                    "404": {
                        "description": "Student not found"
                    }
                }
            }
        }
    },
    "components": {
        "schemas": {
            "Teacher": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "description": "Teacher ID"
                    },
                    "name": {
                        "type": "string",
                        "description": "Teacher name"
                    },
                    "email": {
                        "type": "string",
                        "description": "Teacher email"
                    },
                    "subject": {
                        "type": "string",
                        "description": "Subject taught"
                    },
                    "links": {
                        "type": "object",
                        "properties": {
                            "self": {
                                "type": "string",
                                "description": "Link to this teacher"
                            },
                            "collection": {
                                "type": "string",
                                "description": "Link to all teachers"
                            }
                        }
                    }
                },
                "required": ["name", "email", "subject"]
            },
            "Class": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "Class ID"
                    },
                    "capacity": {
                        "type": "integer",
                        "description": "Class capacity"
                    },
                    "teacher_id": {
                        "type": "integer",
                        "description": "Teacher ID"
                    },
                    "links": {
                        "type": "object",
                        "properties": {
                            "self": {
                                "type": "string",
                                "description": "Link to this class"
                            },
                            "collection": {
                                "type": "string",
                                "description": "Link to all classes"
                            }
                        }
                    }
                },
                "required": ["id", "capacity", "teacher_id"]
            },
            "Student": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "description": "Student ID"
                    },
                    "name": {
                        "type": "string",
                        "description": "Student name"
                    },
                    "email": {
                        "type": "string",
                        "description": "Student email"
                    },
                    "grade": {
                        "type": "string",
                        "description": "Student grade"
                    },
                    "class_id": {
                        "type": "string",
                        "description": "Class ID"
                    },
                    "links": {
                        "type": "object",
                        "properties": {
                            "self": {
                                "type": "string",
                                "description": "Link to this student"
                            },
                            "collection": {
                                "type": "string",
                                "description": "Link to all students"
                            }
                        }
                    }
                },
                "required": ["name", "email", "grade", "class_id"]
            }
        }
    }
} 