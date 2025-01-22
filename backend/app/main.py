from fastapi import FastAPI
from app.cors import add_cors_middleware
from app.routes.recommendations import router as recommendations_router
from app.routes.evaluations import router as evaluations_router
from app.routes.questions import router as questions_router
from app.routes.sales import router as sales_router
from app.routes.resources import router as resources_router
from app.routes.chat import router as chat_router
from app.routes.performance import router as performance_router  

app = FastAPI()
add_cors_middleware(app)

@app.get("/")
async def root():
    return {"message": "Hello, Adaptive Learning Platform is running!"}

app.include_router(recommendations_router, prefix="/api", tags=["recommendations"])
app.include_router(evaluations_router, prefix="/api", tags=["evaluations"])
app.include_router(questions_router, prefix="/api", tags=["questions"])
app.include_router(sales_router, prefix="/api", tags=["sales"])
app.include_router(resources_router, prefix="/api", tags=["resources"])
app.include_router(chat_router, prefix="/api", tags=["chat"])
app.include_router(performance_router, prefix="/api", tags=["performance"])  

