from src.main import calculate_time_back
import time


def test_calculate_time_back():
    """
    Test function to calculate the time back via age.
    """
    age = 3600
    now = int(time.time())
    delta = now - age
    calc = calculate_time_back(age)
    assert calc == delta
