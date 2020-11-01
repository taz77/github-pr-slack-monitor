import os

from hamcrest import *

from src.main import setup_vars


def test_setup_vars_empty():
    """
    Test with no env vars.
    """

    # Call setup_vars with nothing defined to test if error is thrown.
    try:
        setup_vars()
    except Exception as e:
        message = str(e)
    assert_that(message, contains_string("GH_API_TOKEN is not set"))

def test_setup_vars_invalid_url_1():
    """
    Test with invalid URL.
    """
    # Test that the URL is checked to be valid.
    os.environ["GH_API_TOKEN"] = "AAAAAAA"
    os.environ["GH_REPO_NAME"] = "BBBBBBB"
    os.environ["GH_OWNER"] = "CCCCCC"
    os.environ["SLACK_HOOK"] = "DDDDDD"
    os.environ["GH_PR_INTERVAL"] = "10"
    os.environ["GH_PR_THRESH"] = "50"
    try:
        result = setup_vars()
    except Exception as e:
        message = str(e)
    assert_that(message, contains_string("Invalid URL"))

def test_setup_vars_invalid_url_2():
    """
    Test with invalid URL.
    """

    # Test that the URL is checked to be valid.
    os.environ["GH_API_TOKEN"] = "AAAAAAA"
    os.environ["GH_REPO_NAME"] = "BBBBBBB"
    os.environ["GH_OWNER"] = "CCCCCC"
    os.environ["SLACK_HOOK"] = "http://not-a-valid-url.doesnotexist"
    os.environ["GH_PR_INTERVAL"] = "10"
    os.environ["GH_PR_THRESH"] = "50"
    try:
        result = setup_vars()
    except Exception as e:
        message = str(e)
    assert_that(message, contains_string("Invalid URL"))

def test_setup_vars_positive():
    """
    Positive test.
    """
    # Positive test.
    os.environ["GH_API_TOKEN"] = "AAAAAAA"
    os.environ["GH_REPO_NAME"] = "BBBBBBB"
    os.environ["GH_OWNER"] = "CCCCCC"
    os.environ["SLACK_HOOK"] = "https://google.com"
    os.environ["GH_PR_INTERVAL"] = "10"
    os.environ["GH_PR_THRESH"] = "50"
    result = setup_vars()
    assert_that(result['gitrepo'], equal_to("BBBBBBB"))
