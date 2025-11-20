"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# B2B Streaming Platform Schemas

class Channel(BaseModel):
    """
    Channels collection schema
    Collection name: "channel"
    """
    name: str = Field(..., description="Channel display name")
    slug: str = Field(..., description="URL-friendly identifier")
    description: Optional[str] = Field(None, description="Short description")
    logo_url: Optional[HttpUrl] = Field(None, description="Logo image URL")
    categories: List[str] = Field(default_factory=list, description="Categories or tags")
    is_live: bool = Field(False, description="Currently broadcasting live")
    viewer_count: int = Field(0, ge=0, description="Current viewers")

class DemoRequest(BaseModel):
    """
    Demo requests collection schema
    Collection name: "demorequest"
    """
    company: str = Field(..., description="Company name")
    contact_name: str = Field(..., description="Primary contact full name")
    email: str = Field(..., description="Work email")
    use_case: Optional[str] = Field(None, description="Primary streaming use case")
    audience_size: Optional[str] = Field(None, description="Estimated audience size")
    notes: Optional[str] = Field(None, description="Additional context")

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
