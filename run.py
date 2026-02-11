"""Run with: python run.py or uvicorn app.main:app --host 0.0.0.0 --port 8000"""
import os
import uvicorn

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=(os.getenv("ENV") != "production"))
