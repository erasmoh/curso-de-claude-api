from __future__ import annotations

from pydantic import BaseModel


class InvoiceItem(BaseModel):
    description: str
    quantity: float | None = None
    unit_price: float | None = None
    total: float


class InvoiceData(BaseModel):
    provider: str | None
    date: str | None
    currency: str | None
    total: float | None
    items: list[InvoiceItem]
