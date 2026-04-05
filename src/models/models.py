from datetime import datetime, timezone

from sqlalchemy import ForeignKey, BigInteger, JSON, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.models.sqlalchemy_base import Base


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    wallet_address: Mapped[str] = mapped_column(unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), type_=DateTime(timezone=True))


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    signature: Mapped[str] = mapped_column(unique=True, index=True)
    wallet_address: Mapped[str] = mapped_column(
        ForeignKey("subscriptions.wallet_address", ondelete="CASCADE"),
        index=True,
    )
    type: Mapped[str] = mapped_column()
    amount: Mapped[int] = mapped_column(BigInteger)
    from_address: Mapped[str | None]
    to_address: Mapped[str | None]
    token_mint: Mapped[str | None]
    slot: Mapped[int] = mapped_column(BigInteger)
    timestamp: Mapped[int] = mapped_column(BigInteger)
    raw_data: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), type_=DateTime(timezone=True))
