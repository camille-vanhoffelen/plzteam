from typing import Optional

import random
from snekpro.tag_pro_env import TagProExtMultiAgenEnv, AgentAction


class MockTagProExtMutliAgentEnv(TagProExtMultiAgenEnv):
    """This class mocks the TagProExtMultiAgentEnv by mocking all the ExternalMultiAgentEnv
    methods normally made by the rllib package.

    This class can be used to test the integration with the tagpro api and engine,
    """

    def get_action(self, episode_id: str, observation_dict):
        attacker_action = random.choice(list(AgentAction))
        # defender_action = random.choice(list(AgentAction))
        defender_action = AgentAction.NO_PRESS

        action = {
            self._attacker: attacker_action.value,
            self._defender: defender_action.value,
        }

        return action

    def log_returns(self, eid, reward):
        pass
        # print("LOG")

    def end_episode(self, episode_id: str, observation_dict):
        # print("END OF EPISODE")
        pass

    def start_episode(
        self, episode_id: Optional[str] = None, training_enabled: bool = True
    ):
        return "integration_test"
