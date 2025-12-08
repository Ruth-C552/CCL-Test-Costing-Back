from fastapi import FastAPI
from database import engine, Base
from routes import auth_routes
from routes import user_routes
from routes import bench_routes

from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from helpers.http_client import init_client, close_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("Application starting up new...")
    yield
    # Shutdown logic
    print("Application shutting down new...")

origins = [
        "http://localhost",
        "http://localhost:5173",
        "https://your-frontend-domain.com",
    ]


app = FastAPI(title="CCL Test Costing [FastAPI/PostgreSQL]")

app.mount("/static", StaticFiles(directory="uploads"), name="static")

#COR
app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],  # Allows all HTTP methods
        allow_headers=["*"],  # Allows all headers
    )

# include routers
app.include_router(user_routes.router)
app.include_router(auth_routes.router)
app.include_router(bench_routes.router)
# create tables at startup


@app.on_event("startup")
async def startup():
    await init_client()
    async with engine.begin() as conn:
        print("Application starting up old...")
        await conn.run_sync(Base.metadata.create_all)
        
@app.on_event("shutdown")
async def shutdown_event():
    await close_client()
    
def get_httpsx_client():
    return app.state.client