from multiprocessing import Process, Manager, Queue
import time

import snekpro.api as api
from snekpro.integration_tests.mock_tag_pro_env import MockTagProExtMutliAgentEnv


def main():
    print("Starting snekpro")
    manager = Manager()
    game_states = manager.list()
    keypresses = Queue()

    mock_tag_pro_env = MockTagProExtMutliAgentEnv(
        {
            "game_states": game_states,
            "keypresses": keypresses,
        }
    )

    api_process = Process(target=api.run, args=(game_states, keypresses))
    env_process = Process(target=mock_tag_pro_env.run)

    print("Starting API")
    api_process.start()
    time.sleep(5)
    print("Starting agent")
    env_process.start()

    try:
        time.sleep(60)

    except KeyboardInterrupt:
        print("Caught KeyboardInterrupt, terminating processes")
        api_process.terminate()
        api_process.join()
        env_process.terminate()
        env_process.join()
    else:
        print("Timeout, terminating processes")
        api_process.terminate()
        api_process.join()
        env_process.terminate()
        env_process.join()


if __name__ == "__main__":
    main()
