from fastapi import APIRouter, HTTPException, Depends, Query
from datetime import date

from app.database import get_db
from app.models import AttendanceCreate, AttendanceResponse

router = APIRouter(prefix="/api/attendance", tags=["attendance"])

@router.get("", response_model=list[AttendanceResponse])
async def list_attendance(
    employee_id: str | None = Query(None, description="Filter by employee ID"),
    from_date: date | None = Query(None, alias="from_date"),
    to_date: date | None = Query(None, alias="to_date"),
    db=Depends(get_db),
):
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    query = {}
    if employee_id:
        query["employee_id"] = employee_id
    if from_date is not None or to_date is not None:
        date_q = {}
        if from_date is not None:
            date_q["$gte"] = from_date.isoformat()
        if to_date is not None:
            date_q["$lte"] = to_date.isoformat()
        query["date"] = date_q
    cursor = db.attendance.find(query).sort("date", -1)
    records = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        records.append(doc)
    return records

@router.post("", response_model=AttendanceResponse, status_code=201)
async def mark_attendance(attendance: AttendanceCreate, db=Depends(get_db)):
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    employee = await db.employees.find_one({"employee_id": attendance.employee_id})
    if not employee:
        raise HTTPException(
            status_code=404,
            detail=f"Employee with ID '{attendance.employee_id}' not found",
        )
    doc = {
        "employee_id": attendance.employee_id,
        "date": attendance.date.isoformat(),
        "status": attendance.status.value,
    }
    result = await db.attendance.insert_one(doc)
    doc["_id"] = result.inserted_id
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc

@router.get("/summary/{employee_id}")
async def attendance_summary(employee_id: str, db=Depends(get_db)):
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    total_present = await db.attendance.count_documents(
        {"employee_id": employee_id, "status": "Present"}
    )
    total_absent = await db.attendance.count_documents(
        {"employee_id": employee_id, "status": "Absent"}
    )
    return {
        "employee_id": employee_id,
        "total_present_days": total_present,
        "total_absent_days": total_absent,
    }
