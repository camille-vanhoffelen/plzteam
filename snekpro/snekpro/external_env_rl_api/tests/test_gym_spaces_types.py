# pylint: disable=unused-import
import pytest

import gym
import pydantic
from pydantic import BaseModel
from pydantic import ValidationError

from gym_spaces_types import GymDiscrete, gym_discrete


GYM_DISCRETE_N = 5


class GymDiscreteModel(BaseModel):
    value: gym_discrete(n=GYM_DISCRETE_N)


def test_gym_discrete():
    model = GymDiscreteModel(value=1)
    assert model.value == 1
    assert model.value.gym_spaces_class == gym.spaces.Discrete


def test_gym_discrete_wrong_type():
    with pytest.raises(ValidationError) as exc_info:
        GymDiscreteModel(value="this is not an int")

    assert exc_info.value.errors() == [
        {
            "loc": ("value",),
            "msg": "value is not a valid integer",
            "type": "type_error.integer",
        }
    ]


@pytest.mark.parametrize("value", [-1, 5, 6, 7])
def test_gym_discrete_value_not_in_range(value):
    with pytest.raises(ValidationError) as exc_info:
        GymDiscreteModel(value=value)

    assert exc_info.value.errors() == [
        {
            "loc": ("value",),
            "msg": f'value: "{value}" not within range [0, {GYM_DISCRETE_N})',
            "type": "value_error.gymdiscrete",
            "ctx": {"value": value, "n": GYM_DISCRETE_N},
        }
    ]
