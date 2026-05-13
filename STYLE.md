# Documentation
Use markup. This [cheatsheet]([https://sphinx-tutorial.readthedocs.io/cheatsheet](https://gist.github.com/redlotus/3bc387c2591e3e908c9b63b97b11d24e)) may be helpful. You can use `<arg_name> (<type>):` in docstrings if no type hints are used.
Example docstring:
```python
def add(x: int, y) -> int:
  """Adds two integers and returns the result.

  Args:
      x: First of two integers to add
      y (int): Second of two integers to add

  Returns:
      int: result; sum of x and y
  """
  return x + y
```

# Code
tabs or spaces, it doesn't matter.  
I (Sam) prefer to use type hints if possible, but it's totally fine to otherwise simply document the acceptable types in the docstring.  
Two line breaks between root-level function definitions, otherwise use only one line break (like inside functions) wherever you think it helps readability.
