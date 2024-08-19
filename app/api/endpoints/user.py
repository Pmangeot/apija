from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
import jwt
import bcrypt # type: ignore

from models.m_user import User, UserCreate, UserUpdate, UserPasswordUpdate, Token
from datamapper.d_m_user import UserMapper
from core.security import get_current_user, create_access_token, create_refresh_token, SECRET_KEY, ALGORITHM, oauth2_scheme

router = APIRouter()

@router.post("/", response_model=User)
def create_user(user: UserCreate):
    try:
        return UserMapper.create(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = UserMapper.get_by_email(form_data.username)
        if user is None:
            raise HTTPException(status_code=400, detail="Incorrect email or password")

        if not bcrypt.checkpw(form_data.password.encode('utf-8'), user.password.encode('utf-8')):
            raise HTTPException(status_code=400, detail="Incorrect email or password")

        access_token = create_access_token(data={"sub": user.email, "id": user.id, "lastname": user.lastname, "firstname": user.firstname, "admin": user.admin})
        refresh_token = create_refresh_token(data={"sub": user.email})
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/me", response_model=User)
def update_user(user_update: UserUpdate, user: User = Depends(get_current_user)):
    try:
        updated_user = UserMapper.update(user.id, user_update)
        if updated_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return updated_user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/me", response_model=User)
def get_infos_user(user: User = Depends(get_current_user)):
    try:
        infos_user = UserMapper.get_by_id(user.id)
        if infos_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return infos_user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/password", response_model=User)
def update_user_password(user_password_update: UserPasswordUpdate, user: User = Depends(get_current_user)):
    try:
        updated_user = UserMapper.password_update(user.id, user_password_update)
        if updated_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return updated_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id")
        email = payload.get("email")
        if user_id is None or email is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        access_token = create_access_token(data={"sub": email, "id": user_id})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{user_id}")
def delete_all_users(user_id: int, user: User = Depends(get_current_user)):
    if not user.admin or user.id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    try:
        UserMapper.delete_one(user_id)
        return {"message": "User deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/")
def delete_all_users(user: User = Depends(get_current_user)):
    if not user.admin:
        raise HTTPException(status_code=403, detail="Unauthorized")
    try:
        UserMapper.delete_all()
        return {"message": "All users deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
