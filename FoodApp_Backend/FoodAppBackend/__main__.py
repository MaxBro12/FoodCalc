import uvicorn
from fastapi import FastAPI
from routers.v1.endpoints import calculator, minerals, vitamins


app = FastAPI()
app.include_router(calculator.router)
app.include_router(minerals.router)
app.include_router(vitamins.router)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
