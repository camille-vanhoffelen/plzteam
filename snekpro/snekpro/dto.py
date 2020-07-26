from pydantic import BaseModel
from typing import List

class Player(BaseModel):
    player_id: int
    x: float
    dx: float
    y: float
    dy: float

class GameState(BaseModel):
    players: List[Player]


