from pydantic import BaseModel

class TypeBase(BaseModel):
    name: str
    description: str

class TypeCreate(TypeBase):
    pass

class TypeUpdate(TypeBase):
    pass

class Type(TypeBase):
    id: int