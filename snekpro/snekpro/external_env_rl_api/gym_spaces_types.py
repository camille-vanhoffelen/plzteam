from typing import List, Tuple, Type

import pydantic
import gym


class GymDiscreteError(pydantic.PydanticValueError):
    msg_template = 'value: "{value}" not within range [0, {n})'


class GymDiscrete(int):
    n: int
    gym_spaces_class = gym.spaces.Discrete

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            type="integer",
            description=f"gym.spaces.{cls.gym_spaces_class.__name__} type with n={cls.n}",
            gym_spaces_type=cls.gym_spaces_class.__name__,
            n={cls.n},
        )

    @classmethod
    def validate(cls, v, field: "ModelField"):
        pydantic.validators.int_validator(v)

        if v >= field.type_.n or v < 0:
            raise GymDiscreteError(value=v, n=field.type_.n)

        return cls(v)


def gym_discrete(*, n: int) -> GymDiscrete:
    # use kwargs then define conf in a dict to aid with IDE type hinting
    namespace = dict(n=n)
    return type("GymDiscreteValue", (GymDiscrete,), namespace)


class GymDiscrete(int):
    n: int
    gym_spaces_class = gym.spaces.Discrete

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            type="integer",
            description=f"gym.spaces.{cls.gym_spaces_class.__name__} type with n={cls.n}",
            gym_spaces_type=cls.gym_spaces_class.__name__,
            n={cls.n},
        )

    @classmethod
    def validate(cls, v, field: "ModelField"):
        pydantic.validators.int_validator(v)

        if v >= field.type_.n or v < 0:
            raise GymDiscreteError(value=v, n=field.type_.n)

        return cls(v)


def gym_discrete(*, n: int) -> GymDiscrete:
    # use kwargs then define conf in a dict to aid with IDE type hinting
    namespace = dict(n=n)
    return type("GymDiscreteValue", (GymDiscrete,), namespace)
