from fastapi import FastAPI
from src.api.api_v1.routers import api_router
from src.db.base import Base
from src.db.session import engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(api_router)


Base.metadata.create_all(bind=engine)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/healthy')
def health_check():
    return {'status': 'Healthy'}


@app.get("/", status_code=200)
async def root() -> dict:
    return {"message": "Hello World"}