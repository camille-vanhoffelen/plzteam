from multiprocessing import Process, Manager, Queue
import time
import api
import agent


def main():
    """main.

    Snek side process manager.
    Runs the api process, including sneklisten and snekspeak endpoints.
    Runs the agent process, which decides on actions based on game states.
    These two processes communicate through:
    * a game_states list, continuously updated with latest game states from tagpro server
    * a keypresses queue, consumed by snekspeak and forwarded to tagpro server
    """
    print("Starting snekpro")
    manager = Manager()
    game_states = manager.list()
    keypresses = Queue()

    api_process = Process(target=api.run, args=(game_states, keypresses))
    agent_process = Process(target=agent.run, args=(game_states, keypresses))

    print("Starting API")
    api_process.start()
    print("Starting agent")
    agent_process.start()

    try:
        # current shutoff after 60s
        time.sleep(60)

    except KeyboardInterrupt:
        print("Caught KeyboardInterrupt, terminating processes")
        api_process.terminate()
        api_process.join()
        agent_process.terminate()
        agent_process.join()
    else:
        print("Timeout, terminating processes")
        api_process.terminate()
        api_process.join()
        agent_process.terminate()
        agent_process.join()


if __name__ == "__main__":
    main()
