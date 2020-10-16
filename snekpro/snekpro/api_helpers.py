import time
import uuid


KEYPRESS_TIMEOUT = 0.1


def reset_env(game_states, keypresses):
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


def safe_pop_first(game_states):
    try:
        return game_states.pop(0)
    except IndexError:
        return None


def send_action(keypress, keypresses):
    if keypress is None:
        return

    keydown_string = f"event: keydown\ndata: {keypress}\n\n"
    keypresses.put_nowait(keydown_string)
    time.sleep(KEYPRESS_TIMEOUT)
    keyup_string = f"event: keyup\ndata: {keypress}\n\n"
    keypresses.put_nowait(keyup_string)
