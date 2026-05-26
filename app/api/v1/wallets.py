from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import CreateWalletRequest
from app.service import wallets as wallets_service
from app.generator import get_db

router = APIRouter()

@router.get("/balance")
def get_balance(wallet_name: str | None = None,db : Session = Depends(get_db)):
    return wallets_service.get_wallet(db,wallet_name)



@router.post("/wallets")  # Removed {name} path parameter since we're using request body
def create_wallet(wallet: CreateWalletRequest,db : Session = Depends(get_db)):
    return wallets_service.create_wallet(db,wallet)