IST 385 Final: Password Generator Application
Program: Sam Wirth, Documentation: Noel Pang

PWMGR is a password management application with a text-based interface, running off of the command line. Its goal is to generate and store highly secure passwords based on the principle of bits of entropy- a password with a high entropy (randomness) value will take longer to break through brute force attacks. However, since randomness makes it difficult to remember, password management applications are a convenient way to enhance security.

The following determine a password's entropy value:
 - number of characters available in the chosen range
 - number of characters in the password

