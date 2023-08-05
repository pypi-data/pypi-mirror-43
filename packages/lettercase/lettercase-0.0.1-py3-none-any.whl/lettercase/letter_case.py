from enum import IntEnum, auto
from typing import Set

_all__ = ["LetterCase", "CAMEL_CASE", "UNDERSCORE_CASE"]


class LetterCase(IntEnum):
    """Supported letter cases.

    - snake_case
    - UPPER_SNAKE_CASE
    - Darwin_Case
    - PascalCase
    - dromedaryCase
    """
    SNAKE = auto()
    UPPER_SNAKE = auto()
    DARWIN = auto()

    PASCAL = auto()
    DROMEDARY = auto()


CAMEL_CASE: Set[LetterCase] = {LetterCase.PASCAL, LetterCase.DROMEDARY}

UNDERSCORE_CASE: Set[LetterCase] = {LetterCase.SNAKE, LetterCase.UPPER_SNAKE, LetterCase.DARWIN}
