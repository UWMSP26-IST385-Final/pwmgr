IST 385 Final: Password Generator Application

Program: Sam Wirth, Documentation: Noel Pang

PWMGR is a password management application with a text-based interface, running off of the command line. It generates passwords based on the principle of bits of entropy and then calculates that number- a password with a high entropy (randomness) value will take longer to break through brute force attacks, and thus, is stronger. However, since randomness makes it difficult to remember, password management applications are a convenient way to enhance security.

Bits of entropy is determined by the equation $E = L \times \log_2(R)$, where:
- $E$ = password entropy
- $R$ = possible range of character types (charsets)
- $L$ = number of characters in the password
- $\log_2(x)$ = mathematical function "log base 2" (what $n$ for $2^n$ gives $x$?)

As an example, a password with 128 bits of entropy would require $2^{128}$ guesses to brute force. 

The charsets used are `uppercase`, `lowercase`, `special`, and `numbers` 0-9. At least one character from each charset is required to be used at least once. 
Password length can be specified and the application accepts a minimum length of 14 chars and maximum of 64.

Function Breakdown:

`make_entropy_map()`: iterates through every combination of every size selection of charsets and populates the returned values into a dictionary

`check_bad_pw(password)`: compares generated password to database of known bad passwords and notifies if found (to be implemented)

`compute_entropy(charset, length)`: calculates and displays the number of bits of entropy for a successfully generated password

`main()`: runs the program in command line mode (executed when the `generator` module is the entrypoint)
