from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr | None = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr | None = None
    created_at: str | None = None
    class Config:
        from_attributes = True

# 登录请求体
class UserLogin(BaseModel):
    username: str
    password: str

# 登录响应体
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"