import random
from time import sleep

keycodes = [37, 38, 39, 40, 65, 87, 68, 83]


def play(game_states, keypresses):
    keypress = random.choice(keycodes)
    keydown_string = f"event: keydown\ndata: {keypress}\n\n"
    keypresses.put_nowait(keydown_string)
    sleep(0.4)
    keyup_string = f"event: keyup\ndata: {keypress}\n\n"
    keypresses.put_nowait(keyup_string)


def run(shared_game_states, shared_keypresses):
    while True:
        play(shared_game_states, shared_keypresses)
