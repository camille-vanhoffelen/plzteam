from pprint import pprint
from typing import List, Tuple

import gym
import numpy as np
from pydantic import BaseModel, create_model

from fastapi import FastAPI, Query, Path

from pydantic import BaseModel, ValidationError
from pydantic.fields import ModelField
from typing import TypeVar, Generic

import re

# # https://en.wikipedia.org/wiki/Postcodes_in_the_United_Kingdom#Validation
# post_code_regex = re.compile(
#     r"(?:"
#     r"([A-Z]{1,2}[0-9][A-Z0-9]?|ASCN|STHL|TDCU|BBND|[BFS]IQQ|PCRN|TKCA) ?"
#     r"([0-9][A-Z]{2})|"
#     r"(BFPO) ?([0-9]{1,4})|"
#     r"(KY[0-9]|MSR|VG|AI)[ -]?[0-9]{4}|"
#     r"([A-Z]{2}) ?([0-9]{2})|"
#     r"(GE) ?(CX)|"
#     r"(GIR) ?(0A{2})|"
#     r"(SAN) ?(TA1)"
#     r")"
# )


# class PostCode(str):
#     """
#     Partial UK postcode validation. Note: this is just an example, and is not
#     intended for use in production; in particular this does NOT guarantee
#     a postcode exists, just that it has a valid format.
#     """

#     @classmethod
#     def __get_validators__(cls):
#         # one or more validators may be yielded which will be called in the
#         # order to validate the input, each validator will receive as an input
#         # the value returned from the previous validator
#         yield cls.validate

#     @classmethod
#     def __modify_schema__(cls, field_schema):
#         # __modify_schema__ should mutate the dict it receives in place,
#         # the returned value will be ignored
#         field_schema.update(
#             # simplified regex here for brevity, see the wikipedia link above
#             pattern="^[A-Z]{1,2}[0-9][A-Z0-9]? ?[0-9][A-Z]{2}$",
#             # some example postcodes
#             examples=["SP11 9DG", "w1j7bu"],
#         )

#     @classmethod
#     def validate(cls, v):
#         if not isinstance(v, str):
#             raise TypeError("string required")
#         m = post_code_regex.fullmatch(v.upper())
#         if not m:
#             raise ValueError("invalid postcode format")
#         # you could also return a string here which would mean model.post_code
#         # would be a string, pydantic won't care but you could end up with some
#         # confusion since the value's type won't match the type annotation
#         # exactly
#         return cls(f"{m.group(1)} {m.group(2)}")

#     def __repr__(self):
#         return f"PostCode({super().__repr__()})"


class GymDiscrete(gym.spaces.Discrete):
    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        # __modify_schema__ should mutate the dict it receives in place,
        # the returned value will be ignored
        field_schema.update(
            type="integer"
            #     # simplified regex here for brevity, see the wikipedia link above
            #     # pattern="^[A-Z]{1,2}[0-9][A-Z0-9]? ?[0-9][A-Z]{2}$",
            #     # some example postcodes
            # examples=["SP11 9DG", "w1j7bu"],
        )

    @classmethod
    def validate(cls, v):
        # if not isinstance(v, gym.spaces.Discrete):
        # raise TypeError("gym.spaces.Discrete required")
        # m = post_code_regex.fullmatch(v.upper())
        # if not m:
        #     raise ValueError("invalid postcode format")
        # you could also return a string here which would mean model.post_code
        # would be a string, pydantic won't care but you could end up with some
        # confusion since the value's type won't match the type annotation
        # exactly
        aa = cls(v)
        return 1


class Model(BaseModel):
    gym_discrete: GymDiscrete


class Position(BaseModel):
    x: float
    y: float


class Velocity(BaseModel):
    dx: float
    dy: float


class Car(BaseModel):
    position: Position
    velocity: Velocity


class TrafficLight(BaseModel):
    # value: gym.spaces.Discrete(5)
    value: Tuple[int, int, int]


class ObservationSpace(BaseModel):
    car_0: Car
    car_1: Car
    traffic_light_1: List[int]


class EnvironmentState(BaseModel):
    env_id: str = "test"
    done: int = 1
    obs: ObservationSpace


app = FastAPI()


class FooModel(BaseModel):
    foo: str
    bar: int = 123


BarModel = create_model(
    "BarModel",
    apple="russet",
    banana="yellow",
    __base__=FooModel,
)


@app.put("/")
async def root(env_state: Model):
    return env_state


if __name__ == "__main__":
    defender = "defender"
    attacker = "attacker"

    max_time = None
    max_distance = None

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

    observation_space = gym.spaces.Dict(
        {
            defender: ball_observation_space,
            attacker: ball_observation_space,
        }
    )

    key_space = gym.spaces.Discrete(5)
    action_space = gym.spaces.Dict({defender: key_space, attacker: key_space})

    # agent_1 = Agent(name="agent1", value=1)
    # agent_2 = Agent(name="agent2", value=2)

    obs = {"agent1": {"position": [0, 0]}, "agent2": {"position": [1, 1]}}
    # obs = dict(observation_space)
    # env_state = EnvironmentState(obs=obs)

    # pprint(env_state.dict())
    # print(ObservationSpace(car_1=0, car_0=0, traffic_light_1=(3, 2, 1)))
    # print()
    # print(observation_space)
    # print()
    # print(action_space)

    # print(BaseModel.schema())
    m = Model(gym_discrete=10)
    print(FooModel.schema())
    print(m.schema())
    # print(type(m.gym_discrete))
    a = m.gym_discrete.n
    print(a)