from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
import auth
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SierraCare Clinic Service API",
    description="A FastAPI-Based Platform for Discovering and Managing Local Clinic Services in Sierra Leone.",
    version="1.0.0"
)


@app.get("/")
async def welcome():
    return {
        "message": "Welcome to SierraCare Clinic Service API",
        "description": "Search and manage local clinic services in Sierra Leone"
    }


@app.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=auth.hash_password(user.password),
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.post("/login", response_model=schemas.Token)
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid password")

    access_token = auth.create_access_token(
        data={"sub": db_user.email, "role": db_user.role}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.post("/clinics", response_model=schemas.ClinicResponse, status_code=status.HTTP_201_CREATED)
def create_clinic(clinic: schemas.ClinicCreate, db: Session = Depends(get_db)):
    new_clinic = models.Clinic(
        name=clinic.name,
        location=clinic.location,
        phone=clinic.phone,
        opening_hours=clinic.opening_hours
    )

    db.add(new_clinic)
    db.commit()
    db.refresh(new_clinic)

    return new_clinic


@app.get("/clinics", response_model=List[schemas.ClinicResponse])
def get_all_clinics(db: Session = Depends(get_db)):
    return db.query(models.Clinic).all()


@app.get("/clinics/{clinic_id}", response_model=schemas.ClinicResponse)
def get_clinic_by_id(clinic_id: int, db: Session = Depends(get_db)):
    clinic = db.query(models.Clinic).filter(models.Clinic.id == clinic_id).first()

    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")

    return clinic


@app.put("/clinics/{clinic_id}", response_model=schemas.ClinicResponse)
def update_clinic(clinic_id: int, updated_clinic: schemas.ClinicCreate, db: Session = Depends(get_db)):
    clinic = db.query(models.Clinic).filter(models.Clinic.id == clinic_id).first()

    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")

    clinic.name = updated_clinic.name
    clinic.location = updated_clinic.location
    clinic.phone = updated_clinic.phone
    clinic.opening_hours = updated_clinic.opening_hours

    db.commit()
    db.refresh(clinic)

    return clinic


@app.delete("/clinics/{clinic_id}")
def delete_clinic(clinic_id: int, db: Session = Depends(get_db)):
    clinic = db.query(models.Clinic).filter(models.Clinic.id == clinic_id).first()

    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")

    db.delete(clinic)
    db.commit()

    return {"message": "Clinic deleted successfully"}


@app.post("/services", response_model=schemas.ServiceResponse, status_code=status.HTTP_201_CREATED)
def create_service(service: schemas.ServiceCreate, db: Session = Depends(get_db)):
    clinic = db.query(models.Clinic).filter(models.Clinic.id == service.clinic_id).first()

    if not clinic:
        raise HTTPException(status_code=404, detail="Clinic not found")

    new_service = models.Service(
        service_name=service.service_name,
        description=service.description,
        clinic_id=service.clinic_id
    )

    db.add(new_service)
    db.commit()
    db.refresh(new_service)

    return new_service


@app.get("/services", response_model=List[schemas.ServiceResponse])
def get_all_services(db: Session = Depends(get_db)):
    return db.query(models.Service).all()


@app.get("/services/{service_id}", response_model=schemas.ServiceResponse)
def get_service_by_id(service_id: int, db: Session = Depends(get_db)):
    service = db.query(models.Service).filter(models.Service.id == service_id).first()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    return service


@app.put("/services/{service_id}", response_model=schemas.ServiceResponse)
def update_service(service_id: int, updated_service: schemas.ServiceCreate, db: Session = Depends(get_db)):
    service = db.query(models.Service).filter(models.Service.id == service_id).first()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    service.service_name = updated_service.service_name
    service.description = updated_service.description
    service.clinic_id = updated_service.clinic_id

    db.commit()
    db.refresh(service)

    return service


@app.delete("/services/{service_id}")
def delete_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(models.Service).filter(models.Service.id == service_id).first()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    db.delete(service)
    db.commit()

    return {"message": "Service deleted successfully"}


@app.get("/search/clinics", response_model=List[schemas.ClinicResponse])
def search_clinics(location: str = None, service: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Clinic)

    if location:
        query = query.filter(models.Clinic.location.ilike(f"%{location}%"))

    if service:
        query = query.join(models.Service).filter(models.Service.service_name.ilike(f"%{service}%"))

    results = query.all()

    if not results:
        raise HTTPException(status_code=404, detail="No matching clinics found")

    return results