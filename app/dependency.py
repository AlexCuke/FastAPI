from typing import Generator
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials
from app.models import User
from app.repository import users as users_repository

security=HTTPBearer()

def get_db() -> Generator[Session, None, None]:
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
def get_current_user(credentials:HTTPAuthorizationCredentials=Depends(security), db:Session=Depends(get_db)) ->User:
    login=credentials.credentials
    user=users_repository.get_user_by_login(db,login)
    if not user:
        raise HTTPEXception(status_code=404,detail="User not found")
    return user