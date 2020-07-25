from typing import Optional, List
from time import sleep
import random
from collections import deque
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

app = FastAPI()

# keeps 1000 last game states
game_states = deque(maxlen=1000)

# TODO remove hardcoded urls
origins = [
    "http://localhost:8080",
]

# this allows CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


### SNEK LISTEN ###

class Player(BaseModel):
    player_id: int
    x: float
    dx: float
    y: float
    dy: float

class GameState(BaseModel):
    players: List[Player]


@app.post("/sneklisten/")
async def create_ball_state(game_state: GameState):
    print(game_state)
    game_states.append(game_state)
    return game_state

### SNEK SPEAK ###

def stream_keypresses():
    keypresses = [37, 38, 39, 40, 65, 87, 68, 83]
    while True:
        keypress = random.choice(keypresses)
        keydown_string = f'event: keydown\ndata: {keypress}\n\n'
        yield keydown_string
        sleep(0.4)
        keyup_string = f'event: keyup\ndata: {keypress}\n\n'
        yield keyup_string


@app.get("/snekspeak")
def snekspeak():
    return StreamingResponse(stream_keypresses(), media_type="text/event-stream")
