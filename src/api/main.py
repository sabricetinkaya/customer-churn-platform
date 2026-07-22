from fastapi import FastAPI

from src.api.routers.customers import router as customers_router
from src.api.routers.alerts import router as alerts_router


app = FastAPI(
    title="Customer Churn Risk Monitoring API",
    version="1.0.0",
)

app.include_router(customers_router)
app.include_router(alerts_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}