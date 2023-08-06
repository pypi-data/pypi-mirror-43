"""Utilities for making conversion easier."""

from collections import UserDict
from contextlib import suppress
from functools import wraps
from typing import Any, Callable, Iterable, Iterator, Mapping, MutableMapping, MutableSequence, Optional, Set, TypeVar, Union, overload

from .converters import get_converter
from .letter_case import LetterCaseType

__all__ = ["ConversionMemo", "memo_converter", "convert_iter_items", "mut_convert_items", "mut_convert_keys"]

T = TypeVar("T")


class ConversionMemo(UserDict):
    """Mapping specialised for converter memoization.

    This is a two-way mapping so adding key: value will also add value: key.
    The consequence of this is that the `keys` and `values` methods will return
    identical sets.

    The getitem method is the same as with any normal dictionary, apart from it being two-way, but
    the `get` method automatically converts the text if it doesn't already exist.
    This can also be achieved manually using the `convert` method.

    Since this is a two-way mapping, setting a key to a value will also set the value to the key
    and deleting a key will also remove the converted key.

    Args:
        converter ((str) -> str): Converter to use for conversion.
    """
    converter: Callable[[str], str]

    def __init__(self, converter: Callable[[str], str]) -> None:
        super().__init__()
        self.converter = converter

    def __setitem__(self, text: str, converted_text: str) -> None:
        setter = super().__setitem__
        setter(text, converted_text)
        setter(converted_text, text)

    def __delitem__(self, text: str) -> None:
        converted_text = self.__getitem__(text)
        deleter = super().__delitem__
        deleter(text)
        deleter(converted_text)

    def convert(self, text: str) -> str:
        """Convert a text and add it to the memo.

        Args:
            text: Text to convert
        """
        try:
            value = self[text]
        except KeyError:
            value = self[text] = self.converter(text)

        return value

    # noinspection PyOverloads
    @overload
    def get(self, text: str) -> str:
        ...

    # noinspection PyMethodOverriding
    @overload
    def get(self, text: str, *, convert: bool = True, default: T = None) -> Optional[Union[str, T]]:
        ...

    # noinspection PyMethodOverriding
    def get(self, text: str, *, convert: bool = True, default: T = None) -> Optional[Union[str, T]]:
        """Get the converted text.

        Args:
            text: Text to get the converted text for.
            convert: Whether or not to convert the text.
                This takes effect if the converted text
                is not in the map.
            default: Value to return when the text is not
                in the memo and `convert` is `False`.
                If `convert` is `True`, this value will never
                be returned.
        """
        try:
            return self[text]
        except KeyError:
            if convert:
                return self.convert(text)
            return default


def memo_converter(converter: Callable[[str], str], memo: Union[Mapping[str, str], MutableMapping[str, str]]) -> Callable[[str], str]:
    """Decorator which adds memoization to a converter.

    Args:
        converter: Converter to patch
        memo: Memoization mapping to use. If the mapping is mutable it will automatically be updated with new keys.
    """

    @wraps(converter)
    def decorator(text: str) -> str:
        try:
            return memo[text]
        except KeyError:
            pass

        new_text = converter(text)

        with suppress(Exception):
            memo[text] = new_text

        return new_text

    return decorator


def _get_converter(from_case: Optional[LetterCaseType], to_case: LetterCaseType, memo: Optional[Mapping[str, str]]) -> Callable[[str], str]:
    """Internal utility function to get a patched converter."""
    converter = get_converter(from_case, to_case)
    if not converter:
        if from_case:
            text = f"No converter for {from_case} -> {to_case}"
        else:
            text = f"No general converter to {to_case}"

        raise TypeError(text)

    if memo is not None:
        converter = memo_converter(converter, memo)

    return converter


def convert_iter_items(iterable: Iterable[str], from_case: Optional[LetterCaseType], to_case: LetterCaseType, *,
                       memo: Mapping[str, str] = None) -> Iterator[str]:
    """Patch an iterable so that all items are converted to the case.

    Args:
        iterable: Iterable to convert
        from_case: `LetterCase` to convert from, passing `None` will use a general converter.
        to_case: `LetterCase` to convert to
        memo: Memoization mapping to make conversion faster.
    """
    converter = _get_converter(from_case, to_case, memo)
    return map(converter, iterable)


def mut_convert_items(seq: MutableSequence[str], from_case: Optional[LetterCaseType], to_case: LetterCaseType, *,
                      memo: Mapping[str, str] = None) -> None:
    """Convert all items in a mutable sequence to the given case."""
    converter = _get_converter(from_case, to_case, memo)

    for i, item in enumerate(seq):
        new_item = converter(item)
        if new_item != item:
            seq[i] = new_item


def mut_convert_keys(mapping: MutableMapping[str, Any], from_case: Optional[LetterCaseType], to_case: LetterCaseType, *,
                     memo: Mapping[str, str] = None) -> None:
    """Convert all keys in a mutable mapping to the given case.

    Args:
        mapping: Mapping whose keys are to be converted
        from_case: Specify the case to convert from. If not provided a general converter is used.
        to_case: `LetterCase` to convert to
        memo: Memoization map to use.
    """
    converter = _get_converter(from_case, to_case, memo)

    original_keys: Set[str] = set(mapping.keys())

    for key in original_keys:
        new_key = converter(key)
        if new_key != key:
            mapping[new_key] = mapping.pop(key)
