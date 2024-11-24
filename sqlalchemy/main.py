from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import Base, engine, SessionLocal
from models import ToDoItem
from schemas import ToDoItemCreate, ToDoItemResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/todos/", response_model=ToDoItemResponse)
def create_todo(todo: ToDoItemCreate, db: Session = Depends(get_db)):
    db_todo = ToDoItem(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.get("/todos/", response_model=List[ToDoItemResponse])
def get_todos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    todos = db.query(ToDoItem).offset(skip).limit(limit).all()
    return todos

@app.get("/todos/{todo_id}", response_model=ToDoItemResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(ToDoItem).filter(ToDoItem.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Task not found")
    return todo

@app.put("/todos/{todo_id}", response_model=ToDoItemResponse)
def update_todo(todo_id: int, todo: ToDoItemCreate, db: Session = Depends(get_db)):
    db_todo = db.query(ToDoItem).filter(ToDoItem.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in todo.dict().items():
        setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.delete("/todos/{todo_id}", response_model=dict)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(ToDoItem).filter(ToDoItem.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_todo)
    db.commit()
    return {"detail": "Task deleted"}
