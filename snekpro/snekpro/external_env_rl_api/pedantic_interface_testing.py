from pprint import pprint
from typing import List, Tuple, Type

import gym
import numpy as np
from pydantic import BaseModel, create_model

from fastapi import FastAPI, Query, Path

from pydantic import BaseModel, ValidationError, Field
from pydantic.fields import ModelField
from typing import TypeVar, Generic

import pydantic


def gym_discrete(*, n: int) -> Type[int]:
    # use kwargs then define conf in a dict to aid with IDE type hinting
    namespace = dict(n=n)
    return type("GymDiscreteValue", (GymDiscrete,), namespace)


class GymDiscrete(int):
    n: int

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            type="integer",
            description=f"gym.spaces.Dicrete type with n={cls.n}",
            n={cls.n},
        )

    @classmethod
    def validate(cls, v, field: "ModelField"):
        pydantic.validators.int_validator(v)

        if v >= field.type_.n:
            raise TypeError(f"value: {v} is bigger than {field.type_.n-1}")

        return v


class ObservationSpace(BaseModel):
    defender: gym_discrete(n=10)
    attacker: gym_discrete(n=5)


app = FastAPI()


@app.put("/")
async def root(obs_space: ObservationSpace):

    # return {"test": 1}
    return obs_space


if __name__ == "__main__":
    # aa = gym.spaces.Discrete(5)
    # print(aa.contains(0))
    # a = [0, 0, 0]
    # print(isinstance(a, List[int]))
    # m = ObservationSpace()
    # print()
    obs = ObservationSpace(defender=1, attacker=2)
    print(obs)
    print()
    print(ObservationSpace.schema())
