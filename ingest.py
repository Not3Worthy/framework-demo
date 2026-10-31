import asyncio
import json
from sentence_transformers import SentenceTransformer
#from sqlalchemy.ext.asyncio import AsyncSession
from framework_demo.database import async_session_maker, engine, Base
from framework_demo.model.diagnostic_services import Vehicle, ServiceManual, DiagnosticLog

# Load the free, lightweight local embedding model
encoder = SentenceTransformer("all-MiniLM-L6-v2")

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully.")

async def ingest_data():
    # Ensure tables exist first
    await init_db()

    with open("seed_data.json", "r") as f:
        data = json.load(f)

    async with async_session_maker() as session:
        # 1. Ingest Vehicles
        for vehicle in data["vehicles"]:
            db_vehicle = Vehicle(
                vin=vehicle["vin"],
                model_name=vehicle["model_name"],
                model_year=vehicle["model_year"],
                firmware_version=vehicle["firmware_version"]
            )
            session.add(db_vehicle)

        # 2. Ingest Service Manuals with pgvector Embeddings
        for manual in data["service_manuals"]:
            # Construct a rich semantic context string for embedding
            text_to_embed = (
                f"DTC Code: {manual['dtc_code']} | "
                f"Category: {manual['category']} | "
                f"Title: {manual['title']} | "
                f"Procedure: {manual['content']}"
            )
            vector = encoder.encode(text_to_embed).tolist()

            db_manual = ServiceManual(
                title=manual["title"],
                dtc_code=manual["dtc_code"],
                category=manual["category"],
                content=manual["content"],
                embedding=vector
            )
            session.add(db_manual)

        # 3. Ingest Diagnostic Logs
        for log in data["diagnostic_logs"]:
            # Parse telemetry_snapshot string as JSON if needed
            telemetry = (
                json.loads(log["telemetry_snapshot"]) 
                if isinstance(log["telemetry_snapshot"], str) 
                else log["telemetry_snapshot"]
            )
            db_log = DiagnosticLog(
                vin=log["vin"],
                dtc_code=log["dtc_code"],
                severity=log["severity"],
                telemetry_snapshot=telemetry
            )
            session.add(db_log)

        await session.commit()
        print("Successfully ingested vehicles, service manuals, and diagnostic logs with pgvector embeddings!")

if __name__ == "__main__":
    asyncio.run(ingest_data())