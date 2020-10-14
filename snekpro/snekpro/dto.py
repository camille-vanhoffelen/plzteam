from pydantic import BaseModel
from typing import List, Optional


class Player(BaseModel):
    player_id: int
    x: float
    dx: float
    y: float
    dy: float


class GameState(BaseModel):
    game_id: str
    attacker: Player
    defender: Player
    initial: bool
    final: bool
    winner: Optional[int]
    timer: int
