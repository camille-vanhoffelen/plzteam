import time
import api
import agent
from multiprocessing import Process, Manager, Queue
from collections import deque


def main():
    print("Starting snekpro")
    manager = Manager()
    shared_state = manager.dict({'game_states': deque(maxlen=100)})
    keypresses = Queue()

    api_process = Process(target=api.run, args=(shared_state, keypresses))
    agent_process = Process(target=agent.run, args=(shared_state, keypresses))

    print("Starting API")
    api_process.start()
    print("Starting agent")
    agent_process.start()

    try:
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
