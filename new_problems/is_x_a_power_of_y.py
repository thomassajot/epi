"""
Check if a number is a power of another number

Answer:
- If you do division, make sure to keep track of the modulus. If we have floating values we may get rounding errors
- It is not a valid solution to multiply `y` by itself until we get the value `x` or passed it. Because of overflow,
    we may pass `x`. Not only that but the overflow is not detectable ! So we may overflow to a negative or
    even a positive value. In the worst case
    y^n < x but y^n  < y^n+1 < x due to overflow !! so it is not possible to detect this error
"""


# Time complexity: O(log_y(x))
# Space complexity: O(1)
def is_power_of(x: int, y: int) -> bool:
    while x % y == 0:
        x = x / y
    return x == 1


if __name__ == '__main__':
    assert is_power_of(7, 7)
    assert not is_power_of(6, 7)
    assert is_power_of(7**2, 7)
    assert is_power_of(7**3, 7)
    assert not is_power_of(12, 7)