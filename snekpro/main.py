from typing import Optional
from time import sleep
import random
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

app = FastAPI()

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

class BallState(BaseModel):
    x: float
    dx: float
    y: float
    dy: float


@app.post("/sneklisten/")
async def create_ball_state(ball_state: BallState):
    print(ball_state)
    return ball_state

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
