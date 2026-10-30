from sqlalchemy import Column, Integer, String, Text, JSON
from pgvector.sqlalchemy import Vector
from framework_demo.database import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    vin = Column(String, unique=True, index=True)
    model_name = Column(String)
    model_year = Column(Integer)
    firmware_version = Column(String)

class ServiceManual(Base):
    __tablename__ = "service_manuals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    dtc_code = Column(String, index=True, unique=True)
    category = Column(String)
    content = Column(Text)
    # 384 dimensions for sentence-transformers/all-MiniLM-L6-v2
    embedding = Column(Vector(384)) 

class DiagnosticLog(Base):
    __tablename__ = "diagnostic_logs"

    id = Column(Integer, primary_key=True, index=True)
    vin = Column(String, index=True)
    dtc_code = Column(String, index=True)
    severity = Column(String)
    telemetry_snapshot = Column(JSON)