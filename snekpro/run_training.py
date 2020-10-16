from multiprocessing import Process, Manager, Queue
import time
import os

import ray
from ray import tune
from ray.tune import grid_search
from ray.rllib.utils.framework import try_import_tf, try_import_torch
from ray.rllib.utils.test_utils import check_learning_achieved

from snekpro.tag_pro_env import TagProExtMultiAgenEnv
import snekpro.api as api

tf1, tf, tfv = try_import_tf()
torch, nn = try_import_torch()


def get_spaces():
    env = TagProExtMultiAgenEnv(
        {
            "game_states": None,
            "keypresses": None,
        }
    )
    action_space = env.action_space
    obs_space = env.observation_space
    return action_space, obs_space


if __name__ == "__main__":

    as_test = True
    torch = True

    print("Starting snekpro")
    manager = Manager()
    game_states = manager.list()
    keypresses = Queue()

    ray.init()

    action_space, obs_space = get_spaces()

    # documentation uses lambda, no idea why
    policy_mapping = (
        lambda agent_id: "attacker" if agent_id.startswith("attacker") else "defender"
    )

    config = {
        "env": TagProExtMultiAgenEnv,
        "env_config": {
            "game_states": game_states,
            "keypresses": keypresses,
        },
        # Use GPUs iff `RLLIB_NUM_GPUS` env var set to > 0.
        "num_gpus": int(os.environ.get("RLLIB_NUM_GPUS", "0")),
        "num_sgd_iter": 10,
        "lr": grid_search([1e-2, 1e-4, 1e-6]),  # try different lrs
        "num_workers": 0,  # parallelism
        "framework": "tf",
        "multiagent": {
            "policies": {
                # the first tuple value is None -> uses default policy
                "attacker": (None, obs_space, action_space, {"gamma": 0.85}),
                "defender": (None, obs_space, action_space, {"gamma": 0.99}),
            },
            "policy_mapping_fn": policy_mapping,
        },
    }

    stop = {"episodes_total": 10}

    api_process = Process(target=api.run, args=(game_states, keypresses))
    env_process = Process(
        target=tune.run,
        args=("PPO"),
        kwargs=({"config": config, "stop": stop, "verbose": 1}),
    )

    print("Starting API")
    api_process.start()
    time.sleep(5)
    print("Starting agent")
    # this no work
    env_process.start()

    # maybe need to start doing something like these:
    # https://github.com/ray-project/ray/blob/master/rllib/examples/serving/cartpole_client.py
    # https://github.com/ray-project/ray/blob/master/rllib/examples/serving/cartpole_server.py

    # here shitty doc
    # https://docs.ray.io/en/stable/rllib-env.html#multi-agent-and-hierarchical

    try:
        while 1:
            pass

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

    # if as_test:
    # check_learning_achieved(results, 0.1)

    ray.shutdown()