from enum import Enum


class Parks(Enum):
    MAGIC_KINGDOM = 1, "Magic Kingdom"
    HOLLYWOOD_STUDIOS = 2, "Hollywood Studios"
    EPCOT = 3, "Epcot"
    ANIMAL_KINGDOM = 4, "Animal Kingdom"

    def __new__(cls, *args, **kwargs):
        park = object.__new__(cls)
        park._value_ = args[0]
        return park

    def __init__(self, _: str, pretty_name: str = None):
        self._pretty_name_ = pretty_name

    def __str__(self):
        return self.value

    @property
    def pretty_name(self):
        return self._pretty_name_
