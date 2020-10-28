import random
import time
import uuid
from snekpro.dto import GameState

keycodes = [37, 38, 39, 40, 65, 87, 68, 83]


def play(game_states, keypresses):
    # TODO replace with real RL
    # example of random keypresses + wait
    keypress = random.choice(keycodes)
    keydown_string = f"event: keydown\ndata: {keypress}\n\n"
    keypresses.put_nowait(keydown_string)
    time.sleep(0.4)
    keyup_string = f"event: keyup\ndata: {keypress}\n\n"
    keypresses.put_nowait(keyup_string)


def reset(game_states, keypresses, timeout=10) -> GameState:
    """reset.

    This action resets the game.
    Reset event is placed in keypresses, and asynchronously sent to tag pro server.
    Then waits for first game state after reset, and returns it.

    Parameters
    ----------
    game_states :
        game_states
    keypresses :
        keypresses
    timeout :
        timeout

    Returns
    -------
    GameState
        First game state after reset.

    Raises
    ------
    Exception
        If can't get initial game state after reset

    """
    print("Reset game")
    game_id = str(uuid.uuid4())
    reset_string = f'event: reset\ndata: {{"game_id": "{game_id}"}}\n\n'
    keypresses.put_nowait(reset_string)
    del game_states[:]
    start_time = time.time()
    while time.time() - start_time <= timeout:
        first_state = safe_pop_first(game_states)
        if first_state and first_state.game_id == game_id:
            if first_state.initial:
                return first_state
            else:
                raise Exception("Missed initial state after game reset")
    raise Exception("Timeout: waiting for initial state after game reset")


def run(shared_game_states, shared_keypresses):
    """run.

    Main RL agent loop.

    Parameters
    ----------
    shared_game_states :
        shared_game_states contains latest game information sent by tag pro server.
        Asynchronously updated by sneklisten api thread.
    shared_keypresses :
        shared_keypresses list where to place agent actions.
        These will be sent to tag pro server by snekspeak api thread.
    """
    while True:
        # TODO please replace this with smart RL things.
        # this is a pretend agent that resets game then plays 10 moves then resets again.
        initial_state = reset(shared_game_states, shared_keypresses)
        print(f"Initial state: {initial_state}")
        for i in range(30):
            play(shared_game_states, shared_keypresses)
            current_game_state = shared_game_states[-1]
            if current_game_state.final:
                print(f"Final game state: {current_game_state}")
                break


def safe_pop_first(game_states):
    try:
        return game_states.pop(0)
    except IndexError:
        return None
