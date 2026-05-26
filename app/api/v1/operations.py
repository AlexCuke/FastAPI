from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import OperationRequest
from app.service import operations as operation_service
from app.generator import get_db

router = APIRouter()

@router.post("/operation/income")
def add_income(operation: OperationRequest,db : Session = Depends(get_db)):   
    return operation_service.add_income(operation)

@router.post("/operation/expense")
def add_expense(operation: OperationRequest,db : Session = Depends(get_db)):
    return operation_service.add_expense(operation)