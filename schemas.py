from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RoleCreate(BaseModel):
    name: str
    permissions: str


class AssignRole(BaseModel):
    user_id: int
    role_id: int


class RoleResponse(BaseModel):
    id: int
    name: str
    permissions: str

    class Config:
        from_attributes = True


class DocumentResponse(BaseModel):
    id: int
    title: str
    company_name: str
    document_type: str
    uploaded_by: int
    created_at: datetime

    class Config:
        from_attributes = True


class SearchResponse(BaseModel):
    results: List[DocumentResponse]


class RagSearchRequest(BaseModel):
    query: str


class RagChunkResponse(BaseModel):
    document_id: str
    chunk_text: str
    score: float