# File: python-sample-programs/addition.py
"""A simple Python program to add two numbers.
This program defines a function `addition` that takes two integers as input,
adds them, and returns the result. It also includes a main block to execute the
function with user input.
"""

def addition(a: int, b: int) -> int:
    """Returns the sum of two numbers."""
    print(f"Adding {a} and {b}")
    return a + b

if __name__ == "__main__":
    a = int(input())
    b = int(input())
    result = addition(a, b)
    print(f"The result is: {result}")