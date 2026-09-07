from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import  OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate,UserResponse,TokenResponse    
from app.core.security import get_password_hash, verify_password, create_access_token, decode_access_token,oauth2_scheme


router = APIRouter(prefix="/users", tags=["用户管理"])

def fake_hash(password: str) -> str:
    return "fakehashed" + password
@router.post("/register", response_model=UserResponse,status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)): 
    # 第一步：查一下数据库中是否已经存在相同的用户名或邮箱
    existing_user = db.query(User).filter((User.username == user_data.username)).first()
    # 第二步：如果存在，则抛出异常
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已存在") 
    # 第三步：如果不存在，则创建新用户
    new_user = User(
        username=user_data.username,
        password=get_password_hash(user_data.password),
        email=user_data.email,
    )
    # 第四步：将新用户添加到数据库中
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # 第五步：返回新用户的信息
    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "created_at": new_user.created_at.isoformat()
    }

@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 第一步：查找用户
    user = db.query(User).filter(User.username == form_data.username).first()
    # 第二步：如果用户不存在，则抛出异常
    if not user:
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    # 第三步：验证密码是否正确
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    # 第四步：创建JWT访问令牌
    access_token = create_access_token(data={"sub": user.username})
    # 第五步：返回访问令牌
    return {"access_token": access_token, "token_type": "bearer"}       
# 这个函数是“门禁读卡器”：从请求头里拿到令牌，解析出用户名，去数据库里找对应的用户对象
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    # 第一步：解析令牌，获取用户名
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的令牌", headers={"WWW-Authenticate": "Bearer"})
    # 第二步：从payload中获取用户名
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的令牌", headers={"WWW-Authenticate": "Bearer"})
    # 第三步：根据用户名去数据库中查找用户对象  
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的令牌", headers={"WWW-Authenticate": "Bearer"})
    return user
# 获取当前用户信息
@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):    
    # 直接返回当前用户信息
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "created_at": current_user.created_at.isoformat()  
    }