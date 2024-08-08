from pydantic import BaseModel

class StateBase(BaseModel):
    name: str
    description: str

class StateCreate(StateBase):
    pass

class StateUpdate(StateBase):
    pass

class State(StateBase):
    id: int