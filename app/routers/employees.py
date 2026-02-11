from fastapi import APIRouter, HTTPException, Depends

from app.database import get_db
from app.models import EmployeeCreate, EmployeeResponse

router = APIRouter(prefix="/api/employees", tags=["employees"])

def serialize_employee(doc: dict) -> dict:
    doc["id"] = str(doc.pop("_id"))
    return doc

@router.get("", response_model=list[EmployeeResponse])
async def list_employees(db=Depends(get_db)):
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    cursor = db.employees.find({})
    employees = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        employees.append(doc)
    return employees

@router.post("", response_model=EmployeeResponse, status_code=201)
async def create_employee(employee: EmployeeCreate, db=Depends(get_db)):
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    existing = await db.employees.find_one({"employee_id": employee.employee_id})
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Employee with ID '{employee.employee_id}' already exists",
        )
    doc = {
        "employee_id": employee.employee_id,
        "full_name": employee.full_name,
        "email": employee.email,
        "department": employee.department,
    }
    result = await db.employees.insert_one(doc)
    doc["_id"] = result.inserted_id
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc

@router.delete("/{employee_id}")
async def delete_employee(employee_id: str, db=Depends(get_db)):
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    result = await db.employees.delete_one({"employee_id": employee_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    # Optionally delete attendance records for this employee
    await db.attendance.delete_many({"employee_id": employee_id})
    return {"message": "Employee deleted successfully"}
