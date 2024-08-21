from fastapi import APIRouter, HTTPException, Depends, status
from core.security import get_current_user
from models.m_user import User
from typing import List
from datamapper.d_m_type import TypeMapper
from models.m_type import TypeCreate, Type, TypeUpdate

router = APIRouter()

@router.get("/", response_model=List[Type])
def get_all_types():
    return TypeMapper.get_all()

@router.post("/", response_model=Type, status_code=status.HTTP_201_CREATED)
def create_type(new_type: TypeCreate, user: User = Depends(get_current_user)):
    if not user.admin:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        return TypeMapper.create(new_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{type_id}", response_model=Type)
def update_type(type_id: int, updated_type: TypeUpdate, user: User = Depends(get_current_user)):
    if not user.admin:
        raise HTTPException(status_code=403, detail="Forbidden")
    updated_article = TypeMapper.update(type_id, updated_type)
    if updated_article is None:
        raise HTTPException(status_code=404, detail="Type not found")
    return updated_article

@router.delete("/{type_id}")
def delete_type(type_id: int, user: User = Depends(get_current_user)):
    if not user.admin:
        raise HTTPException(status_code=403, detail="Forbidden")
    if not TypeMapper.delete(type_id):
        raise HTTPException(status_code=404, detail="Type not found")
    return {"message": "Type deleted"}

@router.delete("/")
def delete_all_types(user: User = Depends(get_current_user)):
    if not user.admin:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        TypeMapper.delete_all()
        return {"message": "All types deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))