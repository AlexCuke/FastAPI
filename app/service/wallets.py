# service/wallets.py - исправленный
from app.models import User
from app.schemas import CreateWalletRequest
from app.repository import wallets as wallets_repository
from fastapi import HTTPException
from decimal import Decimal
from sqlalchemy.orm import Session

def get_wallet(db: Session, current_user: User, wallet_name: str | None = None):  
    if wallet_name is None:
        wallets = wallets_repository.get_all_wallets(db, current_user.id)  # Добавлен current_user.id
        total_balance = sum(w.balance for w in wallets)
        return {'total_balance': float(total_balance)}
    if not wallets_repository.is_wallet_exist(db, current_user.id, wallet_name):  # Добавлен current_user.id
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{wallet_name}' not found"
        )
    wallet = wallets_repository.get_value_balance_by_name(db, current_user.id, wallet_name)  # Добавлен current_user.id
    return {'wallet': wallet.name, 'balance': float(wallet.balance)}

def create_wallet(db: Session, current_user: User, wallet: CreateWalletRequest):
    if wallets_repository.is_wallet_exist(db, current_user.id, wallet.wallet_name):  # Добавлен current_user.id
        raise HTTPException(
            status_code=400,
            detail=f"Wallet {wallet.wallet_name} already exists"
        )
    new_wallet = wallets_repository.create_wallet(
        db, 
        wallet.wallet_name, 
        Decimal(str(wallet.initial_balance)),
        current_user.id  # Добавлен user_id
    )
    db.commit()
    return {
        "message": f"Wallet {new_wallet.name} created successfully",
        "wallet": new_wallet.name,
        "balance": float(new_wallet.balance)
    }