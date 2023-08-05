from typing import Callable, Optional

from lettercase import LetterCaseType, get_letter_case
from .dromedary_case import *
from .snake_case import *


def get_converter(from_case: Optional[LetterCaseType], to_case: LetterCaseType) -> Optional[Callable[[str], str]]:
    """Find a converter which converts between the given cases.

    Args:
        :param from_case: `LetterCase` of the original text. If `None` a generic handler will be searched.
        :param to_case: Target `LetterCase`
    """
    from_case = get_letter_case(from_case)
    to_case = get_letter_case(to_case)

    name = f"to_{to_case.name.lower()}_case"

    if from_case is not None:
        name = f"{from_case.name.lower()}_{name}"

    return globals().get(name)


def convert_to(text: str, case: LetterCaseType) -> Optional[str]:
    """Convert the given text to the case."""
    case = get_letter_case(case)

    name = f"to_{case.name.lower()}_case"
    try:
        converter = globals()[name]
    except KeyError:
        return None
    else:
        return converter(text)
