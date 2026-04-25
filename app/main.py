from fastapi import FastAPI, HTTPException
from app.api.routes import router




app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app",reload=True)