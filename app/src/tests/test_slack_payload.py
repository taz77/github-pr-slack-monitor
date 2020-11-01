from src.main import slack_payload
from hamcrest import *


def test_slack_payload():
    """
    Test the dictionary being returned.
    """
    testpull = list()
    testpull.append(57998)
    testpull.append((58989))
    owner = 'testowner'
    repo = 'testrepo'
    agetext = 'my age text'
    color = 'red'
    result = slack_payload(testpull, color, owner, repo, agetext)
    keytext = result['blocks'][0]['text']['text']
    assert_that(keytext, contains_string(":red_circle:"))
    assert_that(keytext, contains_string("2"))
