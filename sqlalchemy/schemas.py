from pydantic import BaseModel

class ToDoItemBase(BaseModel):
    title: str
    description: str | None = None
    is_completed: bool = False

class ToDoItemCreate(ToDoItemBase):
    pass

class ToDoItemResponse(ToDoItemBase):
    id: int

    class Config:
        orm_mode = True
