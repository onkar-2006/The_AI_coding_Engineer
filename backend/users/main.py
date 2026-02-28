import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
import models
from database import engine
from api import router


@asynccontextmanager
async def lifespan(app: FastAPI):
  
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield

app = FastAPI(title="My Neon Backend", lifespan=lifespan)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)