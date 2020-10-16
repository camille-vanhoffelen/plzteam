from enum import Enum
import time
from pprint import pprint

import gym
import numpy as np
from scipy.spatial import distance

from ray.rllib.env.external_multi_agent_env import ExternalMultiAgentEnv

from snekpro.api_helpers import reset_env, send_action


class AgentAction(Enum):
    NO_PRESS = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


class TagProExtMultiAgenEnv(ExternalMultiAgentEnv):
    """This is the multi-agent version of ExternalEnv."""

    _REWARD_COEF = 0.1

    def __init__(self, config):
        """Initialize The TagProMultAgenEnv"""
        print("INIT TAG PRO ENV")
        self._game_states = config["game_states"]
        self._keypresses = config["keypresses"]

        self._attacker = "attacker"
        self._defender = "defender"

        self._max_time = None
        self._max_distance = None

        self._ACTION_TO_KEYPRESS = {
            self._attacker: {
                AgentAction.NO_PRESS: None,
                AgentAction.LEFT: 37,
                AgentAction.UP: 38,
                AgentAction.RIGHT: 39,
                AgentAction.DOWN: 40,
            },
            self._defender: {
                AgentAction.NO_PRESS: None,
                AgentAction.LEFT: 65,
                AgentAction.UP: 87,
                AgentAction.RIGHT: 68,
                AgentAction.DOWN: 83,
            },
        }

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
                self._attacker: ball_observation_space,
                self._defender: ball_observation_space,
            }
        )

        key_space = gym.spaces.Discrete(5)
        self._action_space = gym.spaces.Dict(
            {self._attacker: key_space, self._defender: key_space}
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
        # self._timer = time.time()
        while True:
            action = self.get_action(eid, obs)

            obs, reward, done = self._execute_action(action)
            # pprint(reward)
            self.log_returns(
                eid,
                reward,
            )

            if done:
                self.end_episode(eid, obs)
                obs, self._max_distance, self._max_time = self._reset()
                eid = self.start_episode()
                # self._timer = time.time()

    def _reset(self):
        # Ask Api to reset the game
        game_state = reset_env(self._game_states, self._keypresses)

        obs = self._convert_gamestate_to_obs(game_state)

        # TODO: ASK CAM FOR VALUES
        max_distance = 350
        max_time = 500

        return obs, max_distance, max_time

    def _execute_action(self, action):
        # TODO: CHECK WHO IS ATTACK AND DEFENDER

        attacker_action = AgentAction(action[self._attacker])
        attacker_keypress = self._ACTION_TO_KEYPRESS[self._attacker][attacker_action]

        defender_action = AgentAction(action[self._defender])
        defender_keypress = self._ACTION_TO_KEYPRESS[self._defender][defender_action]

        send_action(attacker_keypress, self._keypresses)
        send_action(defender_keypress, self._keypresses)

        while not self._game_states:
            pass

        game_state = self._game_states[-1]
        obs = self._convert_gamestate_to_obs(game_state)

        done = game_state.final
        time_left = game_state.timer
        winner = game_state.winner

        reward = self._compute_reward(obs, time_left, winner)

        return obs, reward, done

    def _compute_reward(self, obs, time_left, winner):
        ball_distance = distance.euclidean(
            obs[self._attacker]["position"], obs[self._defender]["position"]
        )

        attacker_reward = self._compute_attacker_reward(ball_distance)
        defender_reward = self._compute_defender_reward(time_left)

        reward = {self._attacker: attacker_reward, self._defender: defender_reward}

        return reward

    def _compute_attacker_reward(self, ball_distance):
        reward = self._max_distance - ball_distance
        return self._normalize_reward(reward, self._max_distance)

    def _compute_defender_reward(self, time_left):
        reward = self._max_time - time_left
        return self._normalize_reward(reward, self._max_time)

    def _normalize_reward(self, reward, max_value, min_value=0):
        return (reward - min_value) / (max_value - min_value)

    def _convert_gamestate_to_obs(self, game_state):
        attacker_player = game_state.attacker
        defender_player = game_state.defender

        attacker_ball_obs_space = self._convert_player_to_ball_obs(attacker_player)
        defender_ball_obs_space = self._convert_player_to_ball_obs(defender_player)

        observation_space = {
            self._attacker: attacker_ball_obs_space,
            self._defender: defender_ball_obs_space,
        }

        return observation_space

    def _convert_player_to_ball_obs(self, player):
        position_space = [player.x, player.y]
        veloctiy_space = [player.dx, player.dy]

        ball_observation_space = {
            "position": position_space,
            "velocity": veloctiy_space,
        }

        return ball_observation_space
