import pytest
from datamapper.d_m_season import SeasonMapper
from models.m_season import SeasonCreate

season_id = None
nbr_of_active_season = 0

@pytest.mark.order(1)
def test_create_season():
    global season_id
    season_data = SeasonCreate(
        name="Test Season",
        active=True,
        articles=[]
    )
    new_season = SeasonMapper.create_season(new_season=season_data)
    season_id = new_season.id  
    assert new_season.name == "Test Season"
    assert new_season.active is True

@pytest.mark.order(2)
def test_get_active_season():
    global nbr_of_active_season
    active_seasons = SeasonMapper.get_active_seasons()
    nbr_of_active_season = len(active_seasons) - 1  
    assert active_seasons[nbr_of_active_season].name == "Test Season"
    assert active_seasons[nbr_of_active_season].active is True

@pytest.mark.order(3)
def test_get_all_seasons():
    all_seasons = SeasonMapper.get_all_seasons()
    nbr_of_seasons = len(all_seasons) - 1
    assert nbr_of_active_season < nbr_of_seasons
    assert any(season.name == "Test Season" for season in all_seasons)

@pytest.mark.order(4)
def test_deactivate_season():
    deactivated_season = SeasonMapper.deactivate_season(season_id)
    assert deactivated_season.active is False

@pytest.mark.order(5)
def test_delete_season():
    SeasonMapper.delete_season(season_id)
    active_seasons = SeasonMapper.get_active_seasons()
    assert not any(season.name == "Test Season" for season in active_seasons)
