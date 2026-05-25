from fastapi import HTTPException
from app.schemas import OperationRequest
from app.repository import wallets as wallets_repository

def add_income(operation: OperationRequest):
    # Fixed: is_wallet_exist returns bool, check if False
    if not wallets_repository.is_wallet_exist(operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet {operation.wallet_name} not found"
        )
    
    # Now this returns the new balance (not None)
    new_balance = wallets_repository.add_income(operation.wallet_name, operation.amount)
    
    return {
        "message": "Income added successfully",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": new_balance  # Will now have the actual balance
    }
    
def add_expense(operation: OperationRequest):
    # Fixed: is_wallet_exist returns bool, check if False
    if not wallets_repository.is_wallet_exist(operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet {operation.wallet_name} not found"
        )
    
    balance = wallets_repository.get_value_balance_by_name(operation.wallet_name)
    
    if balance < operation.amount:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient funds. Available: {balance}"
        )
    
    # Now this returns the new balance (not None)
    new_balance = wallets_repository.add_expense(operation.wallet_name, operation.amount)
    
    return {
        "message": "Expense added successfully",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": new_balance  # Will now have the actual balance
    }