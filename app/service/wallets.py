from app.schemas import CreateWalletRequest, OperationRequest
from app.repository import wallets as wallets_repository

def get_wallet(wallet_name: str | None = None):  
    if wallet_name is None:
        wallets=wallets_repository.get_all_wallets()
        return {'total_balance': sum(wallets.values())}  # Fixed: removed colon from key
    if not wallets_repository.is_wallet_exist(wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{wallet_name}' not found"
        )
    balance=wallets_repository.get_value_balance_by_name(wallet_name)
    return {'wallet': wallet_name, 'balance': balance}


def create_wallet(wallet: CreateWalletRequest):
    if wallets_repository.is_wallet_exist(wallet.wallet_name):  # Fixed: use wallet_name instead of name
        raise HTTPException(
            status_code=400,
            detail=f"Wallet {wallet.wallet_name} already exists"
        )
    new_balance=wallets_repository.create_wallet(wallet.wallet_name, wallet.initial_balance)
    return {
        "message": f"Wallet {wallet.wallet_name} created successfully",
        "wallet": wallet.wallet_name,
        "balance": new_balance
    }
