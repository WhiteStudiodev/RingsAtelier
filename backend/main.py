from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from config import settings
from database import create_tables, get_db, Lead
from schemas import LeadCreate, LeadOut
from services.telegram import send_lead_notification


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(title="Rings Atelier Leads API", lifespan=lifespan)

origins = [
    origin.strip()
    for origin in settings.cors_origins.split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}


@app.post("/api/leads", response_model=LeadOut)
async def create_lead(lead_data: LeadCreate, db: Session = Depends(get_db)):
    lead = Lead(
        name=lead_data.name,
        method=lead_data.method,
        contact=lead_data.contact,
        message=lead_data.message,
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)

    await send_lead_notification(lead)

    return lead
