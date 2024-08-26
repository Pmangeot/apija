import pytest
from datamapper.d_m_reservation import ReservationMapper
from models.m_reservation import ReservationCreate, ArticlesInResa
from models.m_article import Article

@pytest.mark.order(1)
def test_create_reservation():
    reservation_data = ReservationCreate(
        articles_total=5,
        user_id=1,
        state_id=1,
        season_id=1,
        articles=[]
    )
    
    new_reservation = ReservationMapper.create_reservation(reservation_data)
    global reservation_id
    reservation_id = new_reservation.id
    assert new_reservation.articles_total == 5
    assert new_reservation.user_id == 1
    assert new_reservation.state_id == 1
    assert new_reservation.season_id == 1

@pytest.mark.order(2)
def test_get_reservation_by_id():
    reservation = ReservationMapper.get_by_id(reservation_id)
    assert reservation is not None
    assert reservation[0].id == reservation_id
    assert reservation[0].articles_total == 5

@pytest.mark.order(3)
def test_get_multi_by_userid():
    reservations = ReservationMapper.get_multi_by_userid(1)
    assert len(reservations) > 0
    assert any(reservation.id == reservation_id for reservation in reservations)

@pytest.mark.order(4)
def test_get_all_reservations():
    all_reservations = ReservationMapper.get_all()
    assert len(all_reservations) > 0
    assert any(reservation.id == reservation_id for reservation in all_reservations)

@pytest.mark.order(5)
def test_delete_reservation():
    is_deleted = ReservationMapper.delete(reservation_id)
    assert is_deleted is True
    deleted_reservation = ReservationMapper.get_by_id(reservation_id)
    assert deleted_reservation is None
