from fastapi import APIRouter
from service import operations as operations_service

from schemas import OperationsRequest

router = APIRouter()

@router.post("/operations/income")
def add_income(operation: OperationsRequest):
    return operations_service.add_income(operation)

@router.post("/operations/expense")
def add_expense(operation: OperationsRequest):
    return operations_service.add_expense(operation)