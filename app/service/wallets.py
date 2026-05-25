from app.schemas import CreateWalletRequest, OperationRequest
from app.repository import wallets as wallets_repository
from app.database import SessionLocal
from fastapi import HTTPException
from decimal import Decimal
def get_wallet(wallet_name: str | None = None):  
    db=SessionLocal()
    try:
        if wallet_name is None:
            wallets=wallets_repository.get_all_wallets(db)
            total_balance = sum(w.balance for w in wallets)
            return {'total_balance': total_balance}  # Fixed: removed colon from key
        if not wallets_repository.is_wallet_exist(db,wallet_name):
            raise HTTPException(
                status_code=404,
                detail=f"Wallet '{wallet_name}' not found"
            )
        wallet=wallets_repository.get_value_balance_by_name(db,wallet_name)
        return {'wallet': wallet.name, 'balance': wallet.balance}
    finally:
        db.close()


def create_wallet(wallet: CreateWalletRequest):
    db=SessionLocal()
    try:
        if wallets_repository.is_wallet_exist(db,wallet.wallet_name):  # Fixed: use wallet_name instead of name
            raise HTTPException(
                status_code=400,
                detail=f"Wallet {db,wallet.wallet_name} already exists"
            )
        new_wallet = wallets_repository.create_wallet(
            db, 
            wallet.wallet_name, 
            Decimal(str(wallet.initial_balance))
        )
        db.commit()
        return {
            "message": f"Wallet {new_wallet.name} created successfully",
            "wallet": new_wallet.name,
            "balance": new_wallet.balance
            }
    finally:
        db.close()