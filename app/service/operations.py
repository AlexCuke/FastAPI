from fastapi import HTTPException
from app.schemas import OperationRequest
from app.repository import wallets as wallets_repository
from app.database import SessionLocal

def add_income(operation: OperationRequest):
    db = SessionLocal()
    try:
        if not wallets_repository.is_wallet_exist(db, operation.wallet_name):
            raise HTTPException(
                status_code=404,
                detail=f"Wallet {operation.wallet_name} not found"
            )
        
        wallet = wallets_repository.add_income(db, operation.wallet_name, operation.amount)
        db.commit()
        return {
            "message": "Income added successfully",
            "wallet": operation.wallet_name,
            "amount": operation.amount,
            "description": operation.description,
            "new_balance": float(wallet.balance)  # <-- ИСПРАВЛЕНО: float()
        }
    finally:
        db.close()

def add_expense(operation: OperationRequest):
    db = SessionLocal()
    try:
        if not wallets_repository.is_wallet_exist(db, operation.wallet_name):
            raise HTTPException(
                status_code=404,
                detail=f"Wallet {operation.wallet_name} not found"
            )
        
        wallet = wallets_repository.get_value_balance_by_name(db, operation.wallet_name)
        
        if float(wallet.balance) < operation.amount:  # <-- ИСПРАВЛЕНО: float()
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient funds. Available: {float(wallet.balance)}"
            )
        
        wallet = wallets_repository.add_expense(db, operation.wallet_name, operation.amount)
        db.commit()
        return {
            "message": "Expense added successfully",
            "wallet": operation.wallet_name,
            "amount": operation.amount,
            "description": operation.description,
            "new_balance": float(wallet.balance)  # <-- ИСПРАВЛЕНО: float()
        }
    finally:
        db.close()