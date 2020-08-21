import random
import time
import uuid

keycodes = [37, 38, 39, 40, 65, 87, 68, 83]

RESET_TIMEOUT = 10
POP_ATTEMPTS = 1000


def play(game_states, keypresses):
    keypress = random.choice(keycodes)
    keydown_string = f"event: keydown\ndata: {keypress}\n\n"
    keypresses.put_nowait(keydown_string)
    time.sleep(0.4)
    keyup_string = f"event: keyup\ndata: {keypress}\n\n"
    keypresses.put_nowait(keyup_string)


def reset(game_states, keypresses):
    print("Reset game")
    game_id = str(uuid.uuid4())
    reset_string = f'event: reset\ndata: {{"game_id": "{game_id}"}}\n\n'
    keypresses.put_nowait(reset_string)
    del game_states[:]
    start_time = time.time()
    while time.time() - start_time <= 10:
        first_state = safe_pop_first(game_states)
        if first_state and first_state.game_id == game_id:
            if first_state.initial:
                return first_state
            else:
                raise Exception("Missed initial state after game reset")
    raise Exception("Timeout: waiting for initial state after game reset")


def run(shared_game_states, shared_keypresses):
    while True:
        initial_state = reset(shared_game_states, shared_keypresses)
        print(f'Initial state: {initial_state}')
        for i in range(10):
            play(shared_game_states, shared_keypresses)


def safe_pop_first(game_states):
    try:
        return game_states.pop(0)
    except IndexError:
        return None
