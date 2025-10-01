# backend/main.py
from fastapi import FastAPI
from .api.routes import router
from .db.database import Base, engine
from .core.config import settings
from fastapi.middleware.cors import CORSMiddleware

# landing page
from fastapi.responses import HTMLResponse

# Create tables if no migration has been performed yet.
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head><title>Crypto Dashboard API</title></head>
        <body style="font-family: sans-serif; margin: 2rem;">
            <h1>🚀 Welcome to the Crypto Dashboard API.</h1>
            <p>Voici les ressources disponibles :</p>
            <ul>
                <li><a href="/docs">Swagger UI</a></li>
                <li><a href="/redoc">ReDoc</a></li>
                <li><a href="/api/crypto/">Endpoint /crypto/</a></li>
            </ul>
        </body>
    </html>
"""

