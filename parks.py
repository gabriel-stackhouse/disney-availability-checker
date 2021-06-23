from enum import Enum


class Park(Enum):
    MAGIC_KINGDOM = "Magic Kingdom"
    HOLLYWOOD_STUDIOS = "Hollywood Studios"
    EPCOT = "Epcot"
    ANIMAL_KINGDOM = "Animal Kingdom"

    def __str__(self):
        return self.value
