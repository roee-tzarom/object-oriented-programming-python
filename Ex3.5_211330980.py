# Assignment 3.5 - Python Programming
# Tasks:
# 1) String processing & list comprehensions (process_text)
# 2) Function with default parameters (repeat_frame)
# + 3 different examples for thr use of repeat_frame (examples_repeat_frame)
# 3) Recursion on digits (digit_sum, count_digit)
# 4) Exceptions, input & lists (process_num)

def process_text(s):
    """Analyze a string and return a small info dict."""
    if s == "":
        # empty string is not allowed
        raise ValueError("Empty string is not allowed")

    vowels = "aeiouAEIOU"

    #count vowels
    num_vowels = 0
    for ch in s:
        if ch in vowels:
            num_vowels += 1

    # list of uppercase letters (list comprehension)
    uppercase_letters = [ch for ch in s if ch.isupper()]

    # word lengths (list comprehension)
    words = s.split()
    words_length = [len(w) for w in words]

    result = {
        "length": len(s),
        "vowels": num_vowels,
        "uppercase_letters": uppercase_letters,
        "words_lengths": words_length,
    }
    return result

def repeat_frame(text, times=3, left='[', right=']'):
    """Return text repeated 'times' times, each wrapped with left/right."""
    if times <= 0:
        result = ""
    else:
        parts = []
        for _ in range(times):
            wrapped = f"{left}{text}{right}"
            parts.append(wrapped)
        result = ", ".join(parts)

    return result

def examples_repeat_frame():
    """Demo for repeat_frame (Task 2)."""

    print (repeat_frame("hi"))

    print (repeat_frame("hello", times=2))

    print (repeat_frame("wow", left="<<", right=">>"))

def digit_sum(n):
    """Return sum of digits of a positive integer n (recursive)."""

    if n < 0:
        raise ValueError("Negative number is not allowed")

    # base case: single digit
    if n < 10:
        return n

    # recursive case (last digit + sum of the rest)
    return (n % 10) + digit_sum(n // 10)

def count_digit(n, d):
    """Return how many times digit d appears in n (recursive)."""

    if n < 0:
        raise ValueError("Negative number is not allow for n")

    if d < 0 or d > 9:
        raise ValueError("d must be a digit 0-9")

    # base case: single digit
    if n < 10:
        return 1 if n == d else 0

    return (1 if (n % 10) == d else 0) + count_digit(n // 10, d)

def process_num():
    """Read ints from user, filter negatives, find max (no built-in max)."""
    while True:
        raw = input("Enter integers separated by spaces: ")
        parts = raw.split()

        try:
            # convert all parts to integers
            numbers = [int(p) for p in parts]
            if not numbers:
                print("You must enter at least one integer, try again.\n")
                continue
            break
        except ValueError:
            print("Invalid input, please enter integers only.\n")

    # list of negative numbers (list comprehension)
    negatives = [n for n in numbers if n < 0]

    # find the largest value manually (no max())
    largest = numbers[0]
    for value in numbers[1:]:
        if value > largest:
            largest = value

    # print results
    print("Original list:", numbers)
    print("Negative numbers:", negatives)
    print("Largest number:", largest)
