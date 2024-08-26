from fastapi.security import OAuth2PasswordBearer
from core.config import settings
import jwt
from jwt import ExpiredSignatureError, DecodeError, InvalidTokenError
import datetime
from fastapi import HTTPException, Depends
from models.m_user import User

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_MINUTES = settings.REFRESH_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/login")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id")
        firstname = payload.get("firstname")
        lastname = payload.get("lastname")
        email = payload.get("sub")
        admin = payload.get("admin")
        if user_id is None or firstname is None or lastname is None or email is None or admin is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = User(id=user_id, firstname=firstname, lastname=lastname, email=email, admin=admin)
        return user
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except (DecodeError, InvalidTokenError):
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def is_admin(user: User = Depends(get_current_user)):
    if not user.admin:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return None

