"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
Each Pydantic model represents a collection in your database.
Class name lowercased becomes the collection name (e.g., Product -> "product").
"""
from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product"
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: Optional[str] = Field(None, description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")
    img: Optional[str] = Field(None, description="Image URL")
    rating: Optional[float] = Field(4.5, ge=0, le=5, description="Average rating 0-5")

class OrderItem(BaseModel):
    id: str = Field(..., description="Product id")
    title: str = Field(..., description="Product title at purchase time")
    price: float = Field(..., ge=0, description="Unit price at purchase time")
    qty: int = Field(..., ge=1, description="Quantity")
    img: Optional[str] = Field(None, description="Image URL")

class Order(BaseModel):
    """
    Orders collection schema
    Collection name: "order"
    """
    items: List[OrderItem] = Field(..., description="List of purchased items")
    total: float = Field(..., ge=0, description="Order total amount")
    createdAt: Optional[datetime] = Field(None, description="Client-side created time (optional)")
