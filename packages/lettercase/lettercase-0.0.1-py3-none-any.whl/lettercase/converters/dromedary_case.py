from collections import deque
from typing import Deque

from lettercase import LetterCase, detect_letter_case

__all__ = ["snake_to_dromedary_case"]


def snake_to_dromedary_case(text: str) -> str:
    """Convert from snake_case to dromedaryCase."""
    if not text:
        return text

    chars: Deque[str] = deque()
    next_is_upper: bool = False
    letter_seen: bool = False

    for c in text:
        if c == "_":
            if letter_seen:
                next_is_upper = True
                continue
        elif c.isalpha():
            letter_seen = True

            if next_is_upper:
                c = c.upper()
                next_is_upper = False

        chars.append(c)

    return "".join(chars)


def to_dromedary_case(text: str) -> str:
    """Detect case and convert to dromedaryCase."""
    possible = detect_letter_case(text)

    if not possible:
        raise TypeError(f"Unsupported letter case: {text}")

    if LetterCase.DROMEDARY in possible:
        return text

    raise TypeError(f"Cannot convert any of {possible} to snake_case")
