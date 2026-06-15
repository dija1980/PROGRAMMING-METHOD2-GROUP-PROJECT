<<<<<<< HEAD
# SierraCare Clinic Service API

SierraCare Clinic Service API is a FastAPI-based REST API designed to help users search and manage local clinic services in Sierra Leone.

## Features

- User registration
- User login with JWT token
- Create, read, update and delete clinics
- Create, read, update and delete clinic services
- Search clinics by location and service
- Swagger UI documentation
- ReDoc documentation
- Database integration
- Dependency injection using Depends(get_db)

## Technologies Used

- Python
- FastAPI
- SQLAlchemy
- SQLite/PostgreSQL
- JWT Authentication
- Swagger UI
- ReDoc

## API Endpoints

### Authentication
- POST /register
- POST /login

### Clinics
- POST /clinics
- GET /clinics
- GET /clinics/{clinic_id}
- PUT /clinics/{clinic_id}
- DELETE /clinics/{clinic_id}

### Services
- POST /services
- GET /services
- GET /services/{service_id}
- PUT /services/{service_id}
- DELETE /services/{service_id}

### Search
- GET /search/clinics

## SDG Alignment

This project supports SDG 3: Good Health and Well-Being by helping people locate clinic services more easily in Sierra Leone.

## How to Run

1. Install dependencies:

```bash
pip install -r requirements.txt
=======
# PROGRAMMING-METHOD2-GROUP-PROJECT
FASTAPI and PostgreSQL-based Clinic Service API for managing Clinics , Services and User authentication in Sierra Leone.
>>>>>>> 06c891b09da96239570892b34e0a0bb3c779460a
