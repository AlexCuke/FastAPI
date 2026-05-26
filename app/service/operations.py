from fastapi import HTTPException
from app.models import User
from app.schemas import OperationRequest
from app.repository import wallets as wallets_repository
from sqlalchemy.orm import Session

def add_income(db: Session, current_user: User, operation: OperationRequest):
    if not wallets_repository.is_wallet_exist(db, current_user.id, operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet {operation.wallet_name} not found"
        )
    
    wallet = wallets_repository.add_income(db, current_user.id, operation.wallet_name, operation.amount)
    db.commit()
    return {
        "message": "Income added successfully",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": float(wallet.balance)
    }

def add_expense(db: Session, current_user: User, operation: OperationRequest):
    if not wallets_repository.is_wallet_exist(db, current_user.id, operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet {operation.wallet_name} not found"
        )
    
    wallet = wallets_repository.get_value_balance_by_name(db, current_user.id, operation.wallet_name)
    
    if float(wallet.balance) < operation.amount:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient funds. Available: {float(wallet.balance)}"
        )
    
    wallet = wallets_repository.add_expense(db, current_user.id, operation.wallet_name, operation.amount)
    db.commit()
    return {
        "message": "Expense added successfully",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": float(wallet.balance)
    }