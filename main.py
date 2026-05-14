"""
ist385 final
"""

import secrets
import string
import math
from itertools import combinations

# TODO: PEP257 & Sphinx compliant docstrings
# TODO: transition from TUI to GUI
# TODO: finish password strength (entropy) checker


CHARSETS = {
    "uppercase": string.ascii_uppercase,
    "lowercase": string.ascii_lowercase,
    "special": string.punctuation,
    "numbers": string.digits,
}


"""
map every possible combination of the charsets above to the number of bits of entropy
per character of a string using the given charset
"""


def make_entropy_map() -> dict[frozenset, float]:
    ret = {}
    # n choose r, for every r such that 0 < r <= n
    # aka iterate thru every combination of every size selection of charsets
    for r in range(1, len(CHARSETS)):
        # each choice is a tuple of keys for the CHARSETS dict
        for choice in combinations(CHARSETS, r):
            size = sum(len(CHARSETS[n]) for n in choice)
            ret[frozenset(choice)] = size
    return ret


ENTROPY: dict[frozenset, float] = make_entropy_map()


def check_bad_pw(pw: str, filename: str = "bad_passwords.txt") -> bool:
    """
    Checks whether a password appears in a text file of known bad passwords.
    """

    try:
        with open(filename, "r", encoding="utf-8") as file:
            bad_passwords = {
                line.strip().lower()
                for line in file
                if line.strip()
            }

        return pw.lower() in bad_passwords

    except FileNotFoundError:
        print(f"Warning: {filename} was not found. Skipping bad password check.")
        return False


def pw_entropy(charset: str, length: int) -> float:
    # TODO: perform calculation inline?
    charset_size = len(set(charset))
    return math.log2(charset_size) * length


def main():
    length: int
    
    #Testing for bad password check function
    #print(check_bad_pw("password"))      # should print True
    #print(check_bad_pw("password123"))   # should print True
    #print(check_bad_pw("X7!mQz29@pL"))   # should print False
    
    while True:
        try:
            length = int(input("Enter desired password length:"))
            if length < 14:
                print("Password length must be 14 characters or greater.\n")
            elif length > 64:
                print("Password length cannot be greater than 64 characters\n")
            else:
                break
        except ValueError:
            print("Please enter a valid integer value.\n")

    # TODO: allow selection of charsets to use
    # TODO: also allow specification of # of characters from "special"
    available_chars = (
        CHARSETS["uppercase"]
        + CHARSETS["lowercase"]
        + CHARSETS["numbers"]
        + CHARSETS["special"]
    )
    password: list[str]
    while True:
        password = []
        
        # TODO: better randomness?
        for _ in range(length):
            password.append(secrets.choice(available_chars))
        
        generated = "".join(char for char in password)
        
        # TODO: replace hardcoded checks
        # also this is gross and there is 100% a better way but wtv
        
        if (
            any(letter in CHARSETS["lowercase"] for letter in password)
            and any(letter in CHARSETS["uppercase"] for letter in password)
            and any(letter in CHARSETS["numbers"] for letter in password)
            and any(letter in CHARSETS["special"] for letter in password)
            and not check_bad_pw(generated)
            
        ):
            break
    
    entropy = pw_entropy(available_chars, len(generated))
    
    print(generated)
    print(f"Password entropy (bits): {entropy}")


if __name__ == "__main__":
    main()
