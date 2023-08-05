from typing import Callable, Optional

from lettercase import LetterCase
from .dromedary_case import *
from .snake_case import *


def get_converter(from_case: Optional[LetterCase], to_case: LetterCase) -> Optional[Callable[[str], str]]:
    """Find a converter which converts between the given cases.

    Args:
        :param from_case: `LetterCase` of the original text. If `None` a generic handler will be searched.
        :param to_case: Target `LetterCase`
    """
    name = f"to_{to_case.name.lower()}_case"

    if from_case is not None:
        name = f"{from_case.name.lower()}_{name}"

    return globals().get(name)


def convert_to(text: str, case: LetterCase) -> Optional[str]:
    """Convert the given text to the case."""
    name = f"to_{case.name.lower()}_case"
    try:
        converter = globals()[name]
    except KeyError:
        return None
    else:
        return converter(text)
