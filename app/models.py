
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Numeric
from app.database import Base


class Wallet(Base):
    __tablename__ = "wallet"
    
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    name:Mapped[str] = mapped_column(String(255))
    balance: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal('0.00'))