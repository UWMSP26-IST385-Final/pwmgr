"""
IST385 Final Project
todo...
"""

import secrets
from typing import Literal
import string
import math
from itertools import combinations

# TODO: PEP257 & "Google style" docstrings
# TODO: transition from TUI to GUI

# Literal type allows static checking of keys into CHARSETS and function parameters
CharsetKey = Literal["uppercase", "lowercase", "special", "numbers"]
CHARSETS: dict[CharsetKey, str] = {
    "uppercase": string.ascii_uppercase,
    "lowercase": string.ascii_lowercase,
    "special": string.punctuation,
    "numbers": string.digits,
}


def make_entropy_map() -> dict[frozenset[CharsetKey], float]:
    """Map every possible combination of CHARSETS to the # of bits of entropy
    per character of a string using the given combination
    """
    ret = {}
    # n choose r, for every r such that 0 < r <= n
    # aka iterate thru every combination of every size selection of charsets
    for r in range(1, len(CHARSETS) + 1):
        # each choice is a tuple of keys for the CHARSETS dict
        for choice in combinations(CHARSETS, r):
            size = sum(len(CHARSETS[n]) for n in choice)
            ret[frozenset(choice)] = math.log2(size)
    return ret


ENTROPY = make_entropy_map()


def check_bad_password(password: str) -> bool:  # TODO: implement known bad pw checking
    """Checks paramater against (todo) dictionary of known bad passwords

    Args:
        password: A password to check against knonw bad passwords

    Returns:
        True if password is known to be bad (found in database), False if not

    """
    return False


def compute_entropy(charset: str | frozenset[CharsetKey], length: int) -> float:
    """Compute entropy of a password of a given length made from the provided character set"""
    # TODO: document
    entropy_per_char: float
    if isinstance(charset, str):
        entropy_per_char = math.log2(len(set(charset)))
    else:
        entropy_per_char = ENTROPY[charset]

    return entropy_per_char * length


def meets_entropy(
    length: int, char_selection: frozenset[CharsetKey], min_entropy: float = 75
) -> bool:
    """Returns if a password of a given length, made of a given set of characters meets
    a minimum entropy value.
    """
    # TODO: document
    return compute_entropy(char_selection, length) >= min_entropy


def generate(
    length: int, char_selection: set[CharsetKey] | None = None
) -> tuple[str, float]:
    """Generate a secure random password with adjustable parameters and strength enforcement."""
    # TODO: document (incl. exceptions)
    # TODO: also allow specification of # of characters from "special"
    if char_selection is None:
        char_selection = {"lowercase", "uppercase", "numbers", "special"}

    if length < 14:
        raise ValueError("Password length must be 14 characters or greater.")
    elif length > 64:
        raise ValueError("Password length cannot be grater than 64 characters.")

    password: list[str]
    available_chars = "".join(CHARSETS[key] for key in char_selection)

    # At least one random choice of each character
    password = [secrets.choice(CHARSETS[key]) for key in char_selection]
    # fill remanining characters
    password.extend(
        secrets.choice(available_chars) for _ in range(length - len(password))
    )
    # NOTE: secrets.SystemRandom().shuffle(password) accomplishes the same and is cleaner, but is platform-dependant
    # see: Fisher-Yates shuffle
    for i in range(length - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        password[i], password[j] = password[j], password[i]

    generated = "".join(char for char in password)
    entropy = compute_entropy(available_chars, length)
    return generated, entropy


def main():
    while True:
        try:
            length = int(input("Enter desired password length: "))
            if length < 14:
                print("Password length must be 14 characters or greater.\n")
            elif length > 64:
                print("Password length cannot be grater than 64 characters\n")
            else:
                break
        except ValueError:
            print("Please enter a valid integer value.\n")

    while True:
        choices = list(CHARSETS.keys())
        selection: set[CharsetKey]
        print()
        print("Generation Settings - Make a comma seperated selection (min. 1):")
        print("\t[1] - Uppercase letters")
        print("\t[2] - Lowercase letters")
        print("\t[3] - Special Characters")
        print("\t[4] - Numbers")
        print()
        try:
            indicies = [int(i) for i in input("Selection: ").split(",")]
            if len(indicies) == 0:
                print("Invalid selection, please make at least one selection")
                continue
            if not all((i - 1) < len(choices) for i in indicies):
                print("Invalid selection, each choice must be in the range (1,4)")
                continue

            selection = {choices[(i - 1)] for i in indicies}
        except ValueError:
            print("Please enter a valid, comma-separated list of numeric choices")
            continue

        if not meets_entropy(length, frozenset(selection)):
            print("Provided configuration and password length is too weak!")
            continue
        break

    result = generate(length, selection)
    print("\n")
    print(f"Your password is: {result[0]}")
    # TODO: human readable password scale
    print(f"Password entropy: {result[1]} bits")


if __name__ == "__main__":
    main()
