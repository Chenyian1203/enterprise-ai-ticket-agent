from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# 密码加密工具
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT 密钥（真实企业这里放在 .env 里，这里写死方便你测试）
SECRET_KEY = "super_secret_enterprise_key_666"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# 告诉 FastAPI，咱们的 Token 是从哪个接口发出去的（下面我们写登录接口）
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 【核心！】获取当前登录用户（如果没带 Token 或者 Token 是假的，直接拦截！）
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的身份验证，请重新登录",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 把传过来的 Token 解开看看
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username  # 验证通过，把用户名返回给后面的代码用
    except JWTError:
        raise credentials_exception