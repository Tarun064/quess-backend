from fastapi import APIRouter, Depends, HTTPException
from datetime import date
from app.database import get_db

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

@router.get("/summary")
async def dashboard_summary(db=Depends(get_db)):
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    
    total_employees = await db.employees.count_documents({})
    total_records = await db.attendance.count_documents({})
    
    today = date.today().isoformat()
    today_present = await db.attendance.count_documents({"date": today, "status": "Present"})
    today_absent = await db.attendance.count_documents({"date": today, "status": "Absent"})
    
    return {
        "total_employees": total_employees,
        "total_attendance_records": total_records,
        "today_stats": {
            "date": today,
            "present": today_present,
            "absent": today_absent,
            "not_marked": max(0, total_employees - (today_present + today_absent))
        }
    }
