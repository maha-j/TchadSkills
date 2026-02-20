# API Documentation for TchadSkills

## Overview
This document provides comprehensive API documentation for the TchadSkills application, detailing the available endpoints, including examples and integration guides.

## Base URL
The base URL for all API endpoints is: `https://api.tchadskills.com/v1`

## Authentication
All API calls require authentication. You must include the `Authorization` header with your bearer token:
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## Endpoints

### 1. Get All Skills
- **Endpoint:** `/skills`
- **Method:** `GET`
- **Description:** Retrieve a list of all skills available in the database.
- **Example Request:**
```
GET /skills HTTP/1.1
Host: api.tchadskills.com
Authorization: Bearer YOUR_ACCESS_TOKEN
```
- **Response Example:**
```json
[
    {
        "id": 1,
        "name": "JavaScript",
        "description": "A versatile programming language for web development."
    },
    {
        "id": 2,
        "name": "Python",
        "description": "A high-level programming language known for its readability."
    }
]
```

### 2. Get Skill by ID
- **Endpoint:** `/skills/{id}`
- **Method:** `GET`
- **Description:** Retrieve detailed information about a specific skill.
- **Example Request:**
```
GET /skills/1 HTTP/1.1
Host: api.tchadskills.com
Authorization: Bearer YOUR_ACCESS_TOKEN
```
- **Response Example:**
```json
{
    "id": 1,
    "name": "JavaScript",
    "description": "A versatile programming language for web development."
}
```

### 3. Create a New Skill
- **Endpoint:** `/skills`
- **Method:** `POST`
- **Description:** Create a new skill entry in the database.
- **Request Body:**
```json
{
    "name": "Ruby",
    "description": "A dynamic, open-source programming language."
}
```
- **Example Request:**
```
POST /skills HTTP/1.1
Host: api.tchadskills.com
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
    "name": "Ruby",
    "description": "A dynamic, open-source programming language."
}
```
- **Response Example:**
```json
{
    "id": 3,
    "name": "Ruby",
    "description": "A dynamic, open-source programming language."
}
```

### 4. Update a Skill
- **Endpoint:** `/skills/{id}`
- **Method:** `PUT`
- **Description:** Update an existing skill entry.
- **Request Body:**
```json
{
    "name": "Ruby",
    "description": "Updated description."
}
```
- **Example Request:**
```
PUT /skills/3 HTTP/1.1
Host: api.tchadskills.com
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
    "name": "Ruby",
    "description": "Updated description."
}
```
- **Response Example:**
```json
{
    "id": 3,
    "name": "Ruby",
    "description": "Updated description."
}
```

### 5. Delete a Skill
- **Endpoint:** `/skills/{id}`
- **Method:** `DELETE`
- **Description:** Delete a skill from the database.
- **Example Request:**
```
DELETE /skills/3 HTTP/1.1
Host: api.tchadskills.com
Authorization: Bearer YOUR_ACCESS_TOKEN
```
- **Response Example:**
```json
{
    "message": "Skill deleted successfully."
}
```

## Integration Guide
To integrate the TchadSkills API into your application, follow these steps:
1. Obtain your Access Token.
2. Include the token in your request headers for authentication.
3. Use the appropriate endpoints based on the operations you wish to perform.

## Conclusion
This API provides a powerful way to interact with TchadSkills data and functionality. For further assistance, please refer to our support documentation.