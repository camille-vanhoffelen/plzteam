import time
import api
import agent
from multiprocessing import Process, Manager, Queue

def main():
    print('Starting snekpro')
    manager = Manager()
    game_states = manager.list()
    keypresses = Queue()

    api_process = Process(target=api.run, args=(game_states, keypresses))
    agent_process = Process(target=agent.run, args=(game_states, keypresses))
    
    print('Starting API')
    api_process.start()
    print('Starting agent')
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
        print('Timeout, terminating processes')
        api_process.terminate()
        api_process.join()
        agent_process.terminate()
        agent_process.join()


if __name__ == "__main__":
    main()

