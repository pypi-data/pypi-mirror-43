from typing import Any, Iterable, Iterator, MutableMapping, MutableSequence, Optional, Set

from .converters import get_converter
from .letter_case import LetterCaseType

__all__ = ["convert_iter_items", "mut_convert_items", "mut_convert_keys"]


def convert_iter_items(iterable: Iterable[str], from_case: Optional[LetterCaseType], to_case: LetterCaseType) -> Iterator[str]:
    """Patch an iterable so that all items are converted to the case."""
    converter = get_converter(from_case, to_case)
    if not converter:
        raise TypeError(f"No converter for {from_case} -> {to_case}")

    return map(converter, iterable)


def mut_convert_items(seq: MutableSequence[str], from_case: Optional[LetterCaseType], to_case: LetterCaseType) -> None:
    """Convert all items in a mutable sequence to the given case."""
    converter = get_converter(from_case, to_case)
    if not converter:
        raise TypeError(f"No converter for {from_case} -> {to_case}")

    for i, item in enumerate(seq):
        new_item = converter(item)
        if new_item != item:
            seq[i] = new_item


def mut_convert_keys(mapping: MutableMapping[str, Any], from_case: Optional[LetterCaseType], to_case: LetterCaseType) -> None:
    """Convert all keys in a mutable mapping to the given case."""
    converter = get_converter(from_case, to_case)

    original_keys: Set[str] = set(mapping.keys())

    for key in original_keys:
        new_key = converter(key)
        if new_key != key:
            mapping[new_key] = mapping.pop(key)
