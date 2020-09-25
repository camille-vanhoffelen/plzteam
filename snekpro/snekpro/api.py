from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import uvicorn
from dto import GameState

game_states = None
keypresses = None

MAX_GAME_STATES = 1000

app = FastAPI()

# TODO remove hardcoded urls
origins = [
    "http://localhost:8080",
]

# this allows CORS
app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"],
)


### SNEK LISTEN ###


@app.post("/sneklisten/")
async def create_ball_state(game_state: GameState):
    # fake deque implementation
    if len(game_states) >= MAX_GAME_STATES:
        game_states.pop(0)
    game_states.append(game_state)
    return game_state


### SNEK SPEAK ###


def stream_keypresses():
    while True:
        yield keypresses.get(True, 30)


@app.get("/snekspeak")
def snekspeak():
    return StreamingResponse(stream_keypresses(), media_type="text/event-stream")


def run(shared_game_states, shared_queue):
    global game_states
    game_states = shared_game_states
    global keypresses
    keypresses = shared_queue
    uvicorn.run("api:app", host="127.0.0.1", port=6969, log_level="info")
