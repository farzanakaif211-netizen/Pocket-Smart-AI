import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")
from fastapi import FastAPI
import asyncio
from datetime import datetime, timedelta

app = FastAPI(title="PocketSmart AI")

active_sessions = {}

class Session:
    def __init__(self):
        self.last_activity = datetime.now()

@app.on_event("startup")
async def setup_session_cleanup():
    print("Initializing services...")
    async def cleanup_expired_sessions():
        while True:
            current_time = datetime.now()
            expired = [u for u, s in active_sessions.items() if (current_time - s.last_activity).total_seconds() > 1800]
            for u in expired:
                if u in active_sessions:
                    del active_sessions[u]
            await asyncio.sleep(300)
    asyncio.create_task(cleanup_expired_sessions())

@app.get("/")
async def root():
    return {"message": "PocketSmart AI is running"}

@app.get("/startup")
async def startup_check():
    return {"status": "Services initialized"}
