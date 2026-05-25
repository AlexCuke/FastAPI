from fastapi import APIRouter
from app.schemas import OperationRequest
from app.service import operations as operation_service

router = APIRouter()

@router.post("/operation/income")
def add_income(operation: OperationRequest):   
    return operation_service.add_income(operation)

@router.post("/operation/expense")
def add_expense(operation: OperationRequest):
    return operation_service.add_expense(operation)