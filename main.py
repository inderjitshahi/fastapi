from fastapi import FastAPI, Query
from enum import Enum
from typing import Optional
from pydantic import BaseModel
app = FastAPI()
#.\env\Scripts\activate
# uvicorn main:app --port=8000 --reload

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items")
async def post():
    return {"message": "from route get items"}

@app.get("/items/{item_id}")
async def get(item_id:int):
    return {"item_id": item_id}

class FoodEnum(str, Enum):
    Pizza = "pizza"
    Pasta = "pasta"
    Burger = "burger"

@app.get("/foods/{food_id}")
async def get(food_id:FoodEnum):
    return {"food_id": food_id}

@app.get("/foods/{food_id}/price")
async def get(food_id:FoodEnum, price:int|None =None):
    return {"food_id": food_id, "price": price}


class Item(BaseModel):
    name: str
    description: str|None  = None
    price: float
    tax: Optional[float] = None

@app.post("/items/")
async def create_item(item: Item,q:str|None =Query(None,max_length=5)):
    item_dict = item.dict()
    if item.tax:
        item_dict.update({"price_with_tax": item.price + item.tax})
    if q:
        item_dict.update({"q": q})
    return {**item_dict}