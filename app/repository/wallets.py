

'''BALANCE: dict[str, float] = {}

def is_wallet_exist(wallet_name:str) -> bool:
    return wallet_name in BALANCE

def add_income(wallet_name:str, amount:float):
    BALANCE[wallet_name] += amount
    return BALANCE[wallet_name]
def add_expense(wallet_name:str, amount:float):
    BALANCE[wallet_name] -= amount
    return BALANCE[wallet_name]
def get_value_balance_by_name(wallet_name:str) -> float:
    return BALANCE[wallet_name]


def get_all_wallets() -> dict[str,float]:
    return BALANCE.copy()

def create_wallet(wallet_name:str, amount:float) -> float:
    BALANCE[wallet_name] = amount
    return BALANCE[wallet_name]'''
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Wallet

from decimal import Decimal
    
def is_wallet_exist(db:Session, wallet_name:str) -> bool:
    return db.query(Wallet).filter(Wallet.name==wallet_name).first() is not None


def add_income(db:Session,wallet_name:str, amount:Decimal) ->Wallet:
        wallet=db.query(Wallet).filter(Wallet.name==wallet_name).first() is not None
        wallet.wallet_name += Decimal(str(amount))
        return wallet


def add_expense(db:Session,wallet_name:str, amount:Decimal):
        wallet=db.query(Wallet).filter(Wallet.name==wallet_name).first() is not None
        wallet.balance -= Decimal(str(amount))
        return wallet



def get_value_balance_by_name(db:Session,wallet_name:str) -> Wallet:
        return db.query(Wallet).filter(Wallet.name==wallet_name).first() is not None




def get_all_wallets(db:Session,) -> list[Wallet]:
        return db.query(Wallet).all()

def create_wallet(db:Session,wallet_name:str, amount:Decimal) -> Wallet:
        wallet=Wallet(name=wallet_name,balance=amount)
        db.add(wallet)
        db.flush()
        return wallet
