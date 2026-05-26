from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator, Field

app = FastAPI()

BALANCE: dict[str, float] = {}

# Pydantic models (Модели)
class OperationRequest(BaseModel):
    wallet_name: str = Field(..., max_length=127)
    amount: float
    description: str | None = Field(None, max_length=127)
    
    @field_validator('amount')
    def amount_must_be_positive(cls, v: float):
        if v <= 0:
            raise ValueError('Amount must be positive')
        return v  # IMPORTANT: must return the value
    
    @field_validator('wallet_name')
    def wallet_name_not_empty(cls, v: str):
        v = v.strip()
        if not v:
            raise ValueError('Wallet name cannot be empty')
        return v  # IMPORTANT: must return the value
        
class CreateWalletRequest(BaseModel):
    wallet_name: str = Field(..., max_length=127)
    initial_balance: float
        
    @field_validator('initial_balance')
    def initial_balance_must_be_positive(cls, v: float):
        if v < 0:
            raise ValueError('Initial balance cannot be negative')
        return v  # IMPORTANT: must return the value
    
    @field_validator('wallet_name')
    def wallet_name_not_empty(cls, v: str):
        v = v.strip()
        if not v:
            raise ValueError('Wallet name cannot be empty')
        return v  # IMPORTANT: must return the value

@app.get("/balance")
def get_balance(wallet_name: str | None = None):
    if wallet_name is None:
        return {'total_balance': sum(BALANCE.values())}  # Fixed: removed colon from key
    if wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{wallet_name}' not found"
        )
    return {'wallet': wallet_name, 'balance': BALANCE[wallet_name]}

@app.post("/wallets")  # Removed {name} path parameter since we're using request body
def create_wallet(wallet: CreateWalletRequest):
    if wallet.wallet_name in BALANCE:  # Fixed: use wallet_name instead of name
        raise HTTPException(
            status_code=400,
            detail=f"Wallet {wallet.wallet_name} already exists"
        )
    BALANCE[wallet.wallet_name] = wallet.initial_balance  # Fixed: use wallet.initial_balance
    return {
        "message": f"Wallet {wallet.wallet_name} created successfully",
        "wallet": wallet.wallet_name,
        "balance": BALANCE[wallet.wallet_name]
    }
    
@app.post("/operation/income")
def add_income(operation: OperationRequest):
    if operation.wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet {operation.wallet_name} not found"
        )
    # Removed redundant amount check since validator already ensures amount > 0
    BALANCE[operation.wallet_name] += operation.amount
    return {
        "message": "Income added successfully",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": BALANCE[operation.wallet_name]
    }

@app.post("/operation/expense")
def add_expense(operation: OperationRequest):
    if operation.wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet {operation.wallet_name} not found"
        )
    if BALANCE[operation.wallet_name] < operation.amount:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient funds. Available: {BALANCE[operation.wallet_name]}"  # Fixed typos
        )
    BALANCE[operation.wallet_name] -= operation.amount
    return {
        "message": "Expense added successfully",  # Fixed typo: Expence -> Expense
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": BALANCE[operation.wallet_name]
    }
    
    
class UserRequest(BaseModel):
    login:str=Field(...,max_length=127)


class UserResponse(UserRequest):
    model_config={"from_attributes":True}
    id: int