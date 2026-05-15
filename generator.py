"""
IST385 Final Project
todo...
"""

import secrets
from typing import Literal
import string
import math
from itertools import combinations

# TODO: "Google style" docstrings
# TODO: transition from TUI to GUI

# Literal type allows static checking of keys into CHARSETS and function parameters
CharsetKey = Literal["uppercase", "lowercase", "special", "numbers"]
CHARSETS: dict[CharsetKey, str] = {
    "uppercase": string.ascii_uppercase,
    "lowercase": string.ascii_lowercase,
    "special": string.punctuation,
    "numbers": string.digits,
}

AMBIGUOUS_CHARS = frozenset("|Il1O0")


def make_entropy_map() -> dict[tuple[frozenset[CharsetKey], bool], float]:
    """Map every possible combination of charsets (and ambiguous char toggle)
    to the number of bits of entropy per character.
    """
    ret = {}
    # n choose r, for every r such that 0 < r <= n
    # aka iterate thru every combination of every size selection of charsets
    for r in range(1, len(CHARSETS) + 1):
        # each choice is a tuple of keys for the CHARSETS dict
        for choice in combinations(CHARSETS, r):
            pool: set[str] = set()
            for c in choice:
                pool.update(CHARSETS[c])
            ambig_pool = pool - AMBIGUOUS_CHARS

            # key into map is (charset combination, avoid_ambiguous) so both outcomes are mapped out
            ret[(frozenset(choice), False)] = math.log2(len(pool))
            ret[(frozenset(choice), True)] = (
                math.log2(len(ambig_pool)) if ambig_pool else 0.0
            )
    return ret


ENTROPY = make_entropy_map()


def min_required_chars(
    selection: set[CharsetKey],
    min_numbers: int = 1,
    min_special: int = 1,
) -> int:
    """Total characters required by per-type minimums for the given selection."""
    return sum(
        max(1, min_numbers)
        if k == "numbers"
        else max(1, min_special)
        if k == "special"
        else 1
        for k in selection
    )


def check_bad_password(password: str) -> bool:  # TODO: implement known bad pw checking
    """Checks paramater against (todo) dictionary of known bad passwords

    Args:
        password: A password to check against knonw bad passwords

    Returns:
        True if password is known to be bad (found in database), False if not

    """
    return False


def compute_entropy(
    char_selection: set[CharsetKey] | frozenset[CharsetKey],
    length: int,
    avoid_ambiguous: bool = False,
) -> float:
    """Compute entropy of a password of a given length made from the provided character set."""
    # TODO: document
    if not char_selection or length <= 0:
        return 0.0
    return ENTROPY[(frozenset(char_selection), avoid_ambiguous)] * length


def meets_entropy(
    length: int,
    char_selection: set[CharsetKey],
    min_entropy: float = 75,
    avoid_ambiguous: bool = False,
) -> bool:
    """Returns if a password of a given length, made of a given set of characters meets
    a minimum entropy value.
    """
    # TODO: document
    return compute_entropy(char_selection, length, avoid_ambiguous) >= min_entropy


def generate(
    length: int,
    char_selection: set[CharsetKey] | None = None,
    min_numbers: int = 1,
    min_special: int = 1,
    avoid_ambiguous: bool = False,
) -> str:
    """Generate a secure random password with adjustable parameters and strength enforcement."""
    # TODO: document (incl. exceptions)
    if char_selection is None:
        char_selection = set(CHARSETS.keys())

    if length < 14:
        raise ValueError("Password length must be 14 characters or greater.")
    elif length > 64:
        raise ValueError("Password length cannot be greater than 64 characters.")

    if not char_selection:
        raise ValueError("At least one character set must be selected.")

    # the "pythonic" way to filter a dictionary
    # creates a filtered copy of CHARSETS including only the provided char_selection
    # allows making indidivdual choices of character type based on provided minimums
    char_pools = {
        key: "".join(
            c for c in CHARSETS[key] if not avoid_ambiguous or c not in AMBIGUOUS_CHARS
        )
        for key in char_selection
    }
    available_chars = "".join(char_pools.values())

    if not available_chars:
        raise ValueError("No available characters to generate password.")

    # at least one character from each charset or set minimum
    password: list[str] = []
    for key, pool in char_pools.items():
        if not pool:
            continue

        required = 1
        if key == "numbers":
            required = max(1, min_numbers)
        elif key == "special":
            required = max(1, min_special)

        password.extend(secrets.choice(pool) for _ in range(required))

    if len(password) > length:
        raise ValueError("Minimum character requirements exceed total password length.")

    # fill remaining characters from combined set
    password.extend(
        secrets.choice(available_chars) for _ in range(length - len(password))
    )

    # NOTE: secrets.SystemRandom().shuffle(password) accomplishes the same and is cleaner, but is platform-dependant
    # shuffle bc y not
    # see: Fisher-Yates shuffle
    for i in range(length - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        password[i], password[j] = password[j], password[i]

    return "".join(password)


def main():
    while True:
        try:
            length = int(input("Enter desired password length: "))
            if length < 14:
                print("Password length must be 14 characters or greater.\n")
            elif length > 64:
                print("Password length cannot be greater than 64 characters\n")
            else:
                break
        except ValueError:
            print("Please enter a valid integer value.\n")

    while True:
        choices = list(CHARSETS.keys())
        selection: set[CharsetKey]
        print()
        print("Generation Settings - Make a comma separated selection (min. 1):")
        print("\t[1] - Uppercase letters")
        print("\t[2] - Lowercase letters")
        print("\t[3] - Special Characters")
        print("\t[4] - Numbers")
        print("\t[5] - Avoid Ambiguous (I, l, 1, O, 0)")
        print()
        try:
            indicies = [int(i) for i in input("Selection: ").split(",")]
            # [5] is a flag for avoid_ambiguous, not a charset index; filter it out before lookup
            avoid_ambig = 5 in indicies
            charset_indices = [i for i in indicies if i != 5]

            if len(charset_indices) == 0:
                print("Invalid selection, please make at least one selection")
                continue
            if not all((i - 1) < len(choices) for i in charset_indices):
                print("Invalid selection, each choice must be in the range (1,4)")
                continue

            selection = {choices[(i - 1)] for i in charset_indices}
        except ValueError:
            print("Please enter a valid, comma-separated list of numeric choices")
            continue

        if not meets_entropy(length, selection, avoid_ambiguous=avoid_ambig):
            print("Provided configuration and password length is too weak!")
            continue
        break

    pwd = generate(length, selection, avoid_ambiguous=avoid_ambig)
    entropy = compute_entropy(selection, length, avoid_ambig)
    print("\n")
    print(f"Your password is: {pwd}")
    # TODO: human readable password scale
    print(f"Password entropy: {entropy:.2f} bits")


if __name__ == "__main__":
    main()
