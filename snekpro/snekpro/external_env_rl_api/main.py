from typing import Optional

from fastapi import FastAPI, Query, Path
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse
from enum import Enum

import time


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def root():
    return """ <!DOCTYPE html>
<html>

<head>
  <title>Our Company</title>
</head>

<body>

  <h1>Welcome to Our Company</h1>
  <h2>Web Site Main Ingredients:</h2>

  <p>Pages (HTML)</p>
  <p>Style Sheets (CSS)</p>
  <p>Computer Code (JavaScript)</p>
  <p>Live Data (Files and Databases)</p>

</body>
</html> """
    # return {"message": "Hello World"}


# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id": item_id}


class Item(BaseModel):
    name: str
    description: Optional[str] = Field(
        None, title="The description of the item", max_length=300
    )
    price: float = Field(..., gt=0, description="The price must be greater than zero")
    tax: Optional[float] = None


class User(BaseModel):
    username: str
    full_name: Optional[str] = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results