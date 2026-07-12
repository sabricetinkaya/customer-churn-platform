from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.dependencies import get_db
from src.database.repository import get_risk_increased_customers
from src.database.schemas import PredictionHistoryResponse


router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("/risk-increased", response_model=list[PredictionHistoryResponse])
def read_risk_increased_alerts(
    db: Session = Depends(get_db),
):
    return get_risk_increased_customers(db)