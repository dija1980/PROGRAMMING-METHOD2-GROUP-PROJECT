from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True


class ClinicCreate(BaseModel):
    name: str
    location: str
    phone: str
    opening_hours: str


class ClinicResponse(BaseModel):
    id: int
    name: str
    location: str
    phone: str
    opening_hours: str

    class Config:
        from_attributes = True


class ServiceCreate(BaseModel):
    service_name: str
    description: str
    clinic_id: int


class ServiceResponse(BaseModel):
    id: int
    service_name: str
    description: str
    clinic_id: int

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str