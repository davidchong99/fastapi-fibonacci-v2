def generate_fibonacci(max_value: int) -> list[int]:
    """Return the Fibonacci sequence including all terms up to max_value (inclusive)."""
    a = 0
    b = 1
    result = [a]
    while b <= max_value:
        result.append(b)
        a, b = b, a + b

    return result
