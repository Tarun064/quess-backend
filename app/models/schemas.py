from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date
from enum import Enum

class AttendanceStatus(str, Enum):
    PRESENT = "Present"
    ABSENT = "Absent"

# Employee
class EmployeeCreate(BaseModel):
    employee_id: str = Field(..., min_length=1, description="Unique employee ID")
    full_name: str = Field(..., min_length=1)
    email: EmailStr
    department: str = Field(..., min_length=1)

class EmployeeResponse(BaseModel):
    id: str
    employee_id: str
    full_name: str
    email: str
    department: str

    class Config:
        from_attributes = True

# Attendance
class AttendanceCreate(BaseModel):
    employee_id: str = Field(..., min_length=1)
    date: date
    status: AttendanceStatus

class AttendanceResponse(BaseModel):
    id: str
    employee_id: str
    date: date
    status: str

    class Config:
        from_attributes = True

# Error response
class ErrorResponse(BaseModel):
    detail: str
