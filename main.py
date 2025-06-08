from fastapi import FastAPI, HTTPException, Path
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional, List
from contextlib import asynccontextmanager

# ✅ MySQL connection string
DATABASE_URL = "mysql+pymysql://root:2846@localhost:3306/mydatabase"

# ✅ Create the database engine
engine = create_engine(DATABASE_URL, echo=True)

# ✅ Define your Item model
class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    is_offer: bool = False

# ✅ Define a model for updates (excluding ID)
class ItemUpdate(SQLModel):
    name: str
    price: float
    is_offer: bool = False

# ✅ Create tables on app startup
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# ✅ Use lifespan event to initialize DB
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

# ✅ FastAPI app instance
app = FastAPI(lifespan=lifespan)

# ✅ Create item
@app.post("/items/", response_model=Item)
def create_item(item: Item):
    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item

# ✅ Read all items
@app.get("/items/", response_model=List[Item])
def read_items():
    with Session(engine) as session:
        items = session.exec(select(Item)).all()
        return items

# ✅ Update an item by ID
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: ItemUpdate):
    with Session(engine) as session:
        db_item = session.get(Item, item_id)
        if not db_item:
            raise HTTPException(status_code=404, detail="Item not found")
        db_item.name = updated_item.name
        db_item.price = updated_item.price
        db_item.is_offer = updated_item.is_offer
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
        return db_item

# ✅ Delete an item by ID
@app.delete("/items/{item_id}")
def delete_item(item_id: int = Path(..., title="The ID of the item to delete")):
    with Session(engine) as session:
        db_item = session.get(Item, item_id)
        if not db_item:
            raise HTTPException(status_code=404, detail="Item not found")
        session.delete(db_item)
        session.commit()
        return {"detail": f"Item with id {item_id} deleted successfully"}
