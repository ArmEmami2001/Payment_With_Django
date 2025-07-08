from ninja import Schema
from typing import Optional

class UserCreateSchema(Schema):
    username: str
    email: str
    password: str

class UserReadSchema(Schema):
    id: int
    username: str
    email: str
    credits: Optional[int] 

class ErrorSchema(Schema):
    """Standard schema for error responses."""
    detail: str