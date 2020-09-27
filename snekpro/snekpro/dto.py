from typing import List
from pydantic import BaseModel


class Player(BaseModel):
    player_id: int
    x: float
    dx: float
    y: float
    dy: float


class GameState(BaseModel):
    players: List[Player]
    initial: bool
    game_id: str
