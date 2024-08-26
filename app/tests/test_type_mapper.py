import pytest
from datamapper.d_m_type import TypeMapper
from models.m_type import TypeCreate, TypeUpdate


def test_create_type():
    type_data = TypeCreate(
        name="Test Type",
        description="Test Description"
    )
    new_type = TypeMapper.create(type_data)
    global type_id
    type_id = new_type.id
    assert new_type.name == "Test Type"
    assert new_type.description == "Test Description"

def test_update_type():
    type_data = TypeUpdate(
        name = "Test Type2",
        description = "Test Description2"
    )
    updated_type = TypeMapper.update(type_id, type_data)
    assert updated_type.name == "Test Type2"
    assert updated_type.description == "Test Description2"

def test_get_type():
    type = TypeMapper.get_by_id(type_id)
    assert type.name == "Test Type2"
    assert type.description == "Test Description2"

def test_get_all_types():
    types = TypeMapper.get_all()
    assert len(types) > 0

def test_delete_type():
    TypeMapper.delete(type_id)
    assert TypeMapper.get_by_id(type_id) is None
