from enum import Enum
import math

import gym
import numpy as np

from ray.rllib.env.external_multi_agent_env import ExternalMultiAgentEnv


class KeyPress(Enum):
    NO_PRESS = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


def euclidian_distance(x, y):
    distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(x, y)]))
    return distance


class TagProEnv(ExternalMultiAgentEnv):
    """This is the multi-agent version of ExternalEnv."""

    _REWARD_COEF = 0.1

    def __init__(self,):
        """Initialize a multi-agent external env.
        ExternalMultiAgentEnv subclasses must call this during their __init__.
        Args:
            action_space (gym.Space): Action space of the env.
            observation_space (gym.Space): Observation space of the env.
            max_concurrent (int): Max number of active episodes to allow at
                once. Exceeding this limit raises an error.
        """

        self._defender = "defender"
        self._attacker = "attacker"

        # [x, y]
        position_space = gym.spaces.Box(
            low=-np.finfo(np.float32).max,
            high=np.finfo(np.float32).max,
            shape=(2,),
            dtype=np.float32,
        )

        # [dx, dy]
        veloctiy_space = gym.spaces.Box(
            low=-np.finfo(np.float32).max,
            high=np.finfo(np.float32).max,
            shape=(2,),
            dtype=np.float32,
        )

        ball_observation_space = gym.spaces.Dict(
            {"position": position_space, "velocity": veloctiy_space}
        )

        self._observation_space = gym.spaces.Dict(
            {"defender": ball_observation_space, "attacker": ball_observation_space}
        )

        key_space = gym.spaces.Discrete(5)
        self._action_space = gym.spaces.Dict(
            {"defender": key_space, "attacker": key_space}
        )

        super().__init__(self._action_space, self._observation_space)

    def run(self):
        """Override this to implement the multi-agent run loop.
        Your loop should continuously:
            1. Call self.start_episode(episode_id)
            2. Call self.get_action(episode_id, obs_dict)
                    -or-
                    self.log_action(episode_id, obs_dict, action_dict)
            3. Call self.log_returns(episode_id, reward_dict)
            4. Call self.end_episode(episode_id, obs_dict)
            5. Wait if nothing to do.
        Multiple episodes may be started at the same time.
        """
        eid = self.start_episode()
        obs, self._max_distance = self._reset()
        while True:
            action = self.get_action(eid, obs)

            obs, reward, done = self._execute_action(action)

            self.log_returns(
                eid, reward,
            )
            if done:
                self.end_episode(eid, obs)
                obs = self._reset()
                eid = self.start_episode()

    def _reset(self):
        #
        return 1, 1

    def _execute_action(self, action):
        attacker_action = action["attacker"]
        defender_action = action["defender"]

        return obs, reward, done, info

    def _compute_reward(self, obs, done):
        attacker_obs = obs["attacker"]
        defender_obs = obs["defender"]

        attacker_pos = attacker_obs["position"]
        defender_pos = defender_obs["positon"]

        x_vector = [attacker_pos[0], defender_pos[0]]
        y_vector = [attacker_pos[1], defender_pos[1]]
        ball_distance = euclidian_distance(x_vector, y_vector)

        attacker_reward = self._compute_attacker_reward(ball_distance)
        pass

    def _compute_attacker_reward(self, ball_distance, time_left):
        reward = (self._max_distance - ball_distance) * time_left
        return reward

    def _compute_defender_reward(self, ball_distance, time_left):
        reward = ball_distance
        return reward

