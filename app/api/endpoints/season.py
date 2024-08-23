from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from datamapper.d_m_season import SeasonMapper
from models.m_season import Season, SeasonCreate, SeasonUpdate
from models.m_user import User
from core.security import get_current_user, is_admin

router = APIRouter()

@router.get("/current", response_model=List[Season], status_code=status.HTTP_200_OK)
def get_current_season(user: User = Depends(get_current_user)):
    try:
        return SeasonMapper.get_active_seasons()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/all", response_model=List[Season], status_code=status.HTTP_200_OK)
def get_all_seasons( user: User = Depends(get_current_user)):
    is_admin(user)
    try:
        seasons = SeasonMapper.get_all_seasons()
        if seasons is None:
            raise HTTPException(status_code=404, detail="No Seasons")
        return seasons
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/new", response_model=Season, status_code=status.HTTP_201_CREATED)
def create_season(new_season: SeasonCreate, user: User = Depends(get_current_user)):
    is_admin(user)
    try:
        has_active_season = SeasonMapper.get_active_seasons()
        if has_active_season: 
            return {"message":"Impossible: a season is still active"}

        seasons = SeasonMapper.create_season(new_season)
        if seasons is None:
            raise HTTPException(status_code=404, detail="Not created")
        return seasons
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/{season_id}/deactivate", response_model=Season, status_code=status.HTTP_200_OK)
def deactivate_season(season_id: int, user: User = Depends(get_current_user)):
    is_admin(user)
    try:
        season = SeasonMapper.deactivate_season(season_id)
        if season is None:
            raise HTTPException(status_code=404, detail="Season not found")
        return season
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))