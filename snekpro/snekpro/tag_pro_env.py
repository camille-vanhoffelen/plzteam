from enum import Enum

import gym
import numpy as np
from scipy.spatial import distance

from ray.rllib.env.external_multi_agent_env import ExternalMultiAgentEnv


class KeyPress(Enum):
    NO_PRESS = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


class TagProExtMultiAgenEnv(ExternalMultiAgentEnv):
    """This is the multi-agent version of ExternalEnv."""

    _REWARD_COEF = 0.1

    def __init__(self,):
        """Initialize The TagProMultAgenEnv
       
        """

        self._defender = self._defender
        self._attacker = self._attacker

        self._max_time = None
        self._max_distance = None

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
            {
                self._defender: ball_observation_space,
                self._attacker: ball_observation_space,
            }
        )

        key_space = gym.spaces.Discrete(5)
        self._action_space = gym.spaces.Dict(
            {self._defender: key_space, self._attacker: key_space}
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
        obs, self._max_distance, self._max_time = self._reset()
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
        # Ask Api to reset the game

        # Get the initial obs, max_distande and max_time
        obs = None
        max_distance = None
        max_time = None

        return obs, max_distance, max_time

    def _execute_action(self, action):
        attacker_action = action[self._attacker]
        defender_action = action[self._defender]

        # Send Action to API

        # Wait For API to return obs from action
        obs = None
        done = None
        time_left = None

        reward = self._compute_reward(obs, time_left, done)

        return obs, reward, done

    def _compute_reward(self, obs, time_left, done):
        ball_distance = distance.euclidean(
            obs[self._attacker]["position"], obs[self._defender]["position"]
        )

        attacker_reward = self._compute_attacker_reward(ball_distance)
        defender_reward = self._compute_defender_reward(time_left)

        reward = {self._attacker: attacker_reward, self._defender: defender_reward}

        return reward

    def _compute_attacker_reward(self, ball_distance):
        reward = self._max_distance - ball_distance
        return reward

    def _compute_defender_reward(self, time_left):
        reward = self._max_time - time_left
        return reward
