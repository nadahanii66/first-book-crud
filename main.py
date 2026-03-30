from fastapi import FastAPI ,Depends, HTTPException, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session  

app = FastAPI()
models.Base.metadata.create_all(bind=engine, checkfirst=True)

class Book(BaseModel):
    title: str
    author:str
    id: int
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/books/", response_model=Book)
async def create_book(book: Book, db: db_dependency):
    db_book = models.Books(**book.dict().values()) # علشان اجيب كل الداتا بتاعتي من البيز مودل مره واحده بدل ما اكتب كل واحده لوحدها
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
@app.get("/books/{book_id}", response_model=Book)
async def read_book(book_id: int, db: db_dependency):
    db_book = db.query(models.Books).filter(models.Books.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return db_book
@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, book: Book, db: db_dependency):
    db_book = db.query(models.Books).filter(models.Books.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    for key, value in book.dict().items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book
@app.delete("/books/{book_id}")
async def delete_book(book_id: int, db: db_dependency):
    db_book = db.query(models.Books).filter(models.Books.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return {"detail": "Book deleted successfully"}
