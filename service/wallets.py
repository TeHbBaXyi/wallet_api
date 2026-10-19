from schemas import CreateWalletRequest
from fastapi import HTTPException
from repository import wallets as wallet_repository

def get_balance(wallet_name: str | None = None):
    if wallet_name is None:
        wallets = wallet_repository.get_all_wallets()
        return {"total_balance": sum(wallets.values())}
    if not wallet_repository.is_wallet_exist(wallet_name):
        raise HTTPException(status_code=404,
                            detail=f"Wallet {wallet_name} not found"
                            )
    balance = wallet_repository.get_wallet_balance_by_name(wallet_name)
    return {"wallet": wallet_name, "balance": balance}


def create_wallet(wallet: CreateWalletRequest):
    if wallet_repository.is_wallet_exist(wallet.name):
        raise HTTPException(
            status_code=400,
            detail=f"Wallet {wallet.name} already exists")
    new_balance = wallet_repository.create_wallet(wallet.name, wallet.initial_balance)
    return {
        "message": f"Wallet {wallet.name} created",
        "wallet": wallet.name,
        "balance": new_balance
    }
