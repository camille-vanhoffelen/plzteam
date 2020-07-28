from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import uvicorn
from dto import GameState

app = FastAPI()

game_states = None
keypresses = None

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
    game_states.put(game_state)
    # print(f'Added game state. size: {len(game_states)}')
    return game_state


### SNEK SPEAK ###


def stream_keypresses():
    while True:
        yield keypresses.get(True, 30)


@app.get("/snekspeak")
def snekspeak():
    return StreamingResponse(stream_keypresses(), media_type="text/event-stream")


def run(shared_state, shared_queue):
    global game_states
    game_states = shared_state
    global keypresses
    keypresses = shared_queue
    uvicorn.run("api:app", host="127.0.0.1", port=6969, log_level="error")
