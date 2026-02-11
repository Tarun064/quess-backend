# HRMS Lite - Backend

## 🚀 Overview
The backend of HRMS Lite is a high-performance **FastAPI** application that provides a robust REST API for managing employee records and attendance. It leverages **MongoDB** for asynchronous data persistence and **Pydantic** for strict data validation.

## 🛠 Tech Stack
- **FastAPI**: Modern, fast (high-performance) web framework for building APIs.
- **Motor**: Asynchronous Python driver for MongoDB.
- **MongoDB**: NoSQL database for flexible and scalable data storage.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **Uvicorn**: Lightning-fast ASGI server implementation.

## 📁 Structure
- `app/main.py`: Entry point and main FastAPI instance.
- `app/database.py`: MongoDB connection and dependency injection.
- `app/routers/`: API endpoints for Employees and Attendance.
- `app/models/schemas.py`: Request and response models (Pydantic).
- `app/config.py`: Environment configuration and settings.

## 📡 API Endpoints

### Employees
- `POST /api/employees`: Register a new employee.
- `GET /api/employees`: List all registered employees.
- `DELETE /api/employees/{id}`: Remove an employee and their records.

### Attendance
- `POST /api/attendance`: Mark attendance (Present/Absent).
- `GET /api/attendance`: Query attendance with filters (`employee_id`, `from_date`, `to_date`).
- `GET /api/attendance/summary/{id}`: Get aggregated statistics for an employee.

## ⚙️ Configuration
The application uses a `.env` file for configuration. Key variables include:
- `MONGODB_URI`: Connection string for your MongoDB instance.
- `DATABASE_NAME`: Name of the database to use.
- `FRONTEND_URL`: CORS origin for the React application.

## 🛠 Setup
1. `pip install -r requirements.txt`
2. Configure `.env` based on `.env.example`.
3. `uvicorn app.main:app --reload`
