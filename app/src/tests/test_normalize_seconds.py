from src.main import normalize_seconds


def test_normalize_seconds():
    """
    Take a number of seconds and test converting it to a human readable time frame.
    """
    n = 451071

    (days, remainder) = divmod(n, 86400)
    (hours, remainder) = divmod(remainder, 3600)
    (minutes, seconds) = divmod(remainder, 60)
    date = normalize_seconds(n)
    assert date.days == days
    assert date.hours == hours
    assert date.minutes == minutes
    assert date.seconds == seconds
