"""Python module to not actually encrypt your text."""

from string import ascii_lowercase as lowercase
from string import ascii_uppercase as uppercase
from string import digits as number
from string import punctuation
from typing import Iterable, Tuple

from argh import ArghParser, arg, wrap_errors


class UnspecifiedBehavior(Exception):
    """Unspecified Behavior"""


def _ischar(char: str) -> bool:
    return len(char) == 1


def _get_overflow_index(base: Iterable, base_index: int) -> int:
    length = len(base)
    index = base_index
    while index >= length:
        index -= length

    while index <= -length:
        index += length
    return index


def _get(iterable: Iterable, overflow_index: int):
    xvalue = _get_overflow_index(iterable, overflow_index)
    return iterable[xvalue]


def encryptf(string: str, charint: Tuple[str, int]) -> str:
    """(Not) Encrypt your text by given tuple that look like this: k=5 # ('k', 5)
    It'll raise error if charint[0] not a lowercase"""
    char = charint[0] if _ischar(charint[0]) else charint[0][0]
    if not char in lowercase:
        raise UnspecifiedBehavior("Not a lowercase char")
    base = charint[1]+lowercase.index(char)
    new_string = ""
    for char_s in string:
        if char_s in lowercase:
            index = lowercase.index(char_s)
            new_string += _get(lowercase, index+base)
            continue
        if char_s in uppercase:
            index = uppercase.index(char_s)
            new_string += _get(uppercase, index+base)
            continue
        if char_s in number:
            index = number.index(char_s)
            new_string += _get(number, index+base)
            continue
        if char_s in punctuation:
            index = punctuation.index(char_s)
            new_string += _get(
                punctuation, index+base)
            continue
        new_string += char_s  # Whitespace?
    return new_string


def decryptf(string: str, charint: Tuple[str, int]):
    """Decrypt the text by [char]=[int # e.g: x=5"""
    char = charint[0] if _ischar(charint[0]) else charint[0][0]
    if not char in lowercase:
        raise UnspecifiedBehavior("Not a lowercase char")
    base = lowercase.index(char)+charint[1]
    new_string = ""

    for char_s in string:
        if char_s in lowercase:
            index = lowercase.index(char_s)
            new_string += _get(lowercase, index-base)
            continue
        if char_s in uppercase:
            index = uppercase.index(char_s)
            new_string += _get(uppercase, index-base)
            continue
        if char_s in number:
            index = number.index(char_s)
            new_string += _get(number, index-base)
            continue
        if char_s in punctuation:
            index = punctuation.index(char_s)
            new_string += _get(punctuation, index-base)
            continue
        new_string += char_s  # Whitespace?
    return new_string


ERRS = [UnspecifiedBehavior, ValueError]


def _proc(exc):
    return f"{type(exc).__name__}: {str(exc)}"


@wrap_errors(ERRS, _proc)
@arg("string", help="String to encrypt or decrypt")
@arg("base", help="Base, e.g: k=5")
@arg("-e", "--encrypt", help="Encrypt mode. If none present, 4ncrypt is used. \
If both present, decrypt is ignored")
@arg("-d", "--decrypt", help="Decrypt mode")
def main(string: str, base: str, encrypt=False, decrypt=False):
    """Encrypt/Decrypt a text by base"""
    if not "=" in base:
        raise UnspecifiedBehavior("Separator is =")
    char, num = base.split("=")
    if not encrypt and not decrypt:
        encrypt = True
    if encrypt:
        return encryptf(string, (char, int(num)))
    return decryptf(string, (char, int(num)))


if __name__ == "__main__":
    # testobj = encrypt("Hello, World", ('k', 20))
    # print(f"Hello, World -> {testobj}")
    # dec_testobj = decrypt(testobj, ('k', 20))
    # print(f"{testobj} -> {dec_testobj}")
    parser = ArghParser()  # pylint: disable
    parser.set_default_command(main)
    parser.dispatch()
