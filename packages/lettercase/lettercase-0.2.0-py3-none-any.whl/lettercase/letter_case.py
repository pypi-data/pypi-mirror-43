from enum import Enum
from typing import Set, Union

_all__ = ["LetterCase", "CAMEL_CASE", "UNDERSCORE_CASE", "LetterCaseType", "get_letter_case"]


class LetterCase(Enum):
    """Supported letter cases.

    - snake_case
    - UPPER_SNAKE_CASE
    - Darwin_Case
    - PascalCase
    - dromedaryCase
    """
    SNAKE = "snake"
    UPPER_SNAKE = "upper_snake"
    DARWIN = "darwin"

    PASCAL = "pascal"
    DROMEDARY = "dromedary"


CAMEL_CASE: Set[LetterCase] = {LetterCase.PASCAL, LetterCase.DROMEDARY}

UNDERSCORE_CASE: Set[LetterCase] = {LetterCase.SNAKE, LetterCase.UPPER_SNAKE, LetterCase.DARWIN}

LetterCaseType = Union[LetterCase, str]


def get_letter_case(case: LetterCaseType) -> LetterCase:
    """Get a `LetterCase` from `LetterCaseType`.

    Raises:
        :raise ValueError: If the passed value is invalid and cannot be resolved to `LetterCase`
        :raise TypeError: If something other than `LetterCaseType` is passed
    """
    try:
        return LetterCase(case)
    except ValueError:
        pass

    if not isinstance(case, str):
        raise TypeError(f"Type {type(case).__name__} can not be used as a LetterCase")

    cleaned_case = case.lower()
    cleaned_case = cleaned_case.partition("_case")[0]

    return LetterCase(cleaned_case)
