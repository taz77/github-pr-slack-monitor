import argparse
import json
import logging
import os
import sys
import time
from collections import defaultdict, namedtuple

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from github import Github

from .__init__ import __version__

parser = argparse.ArgumentParser(
    description='A simple PR monitor for Github to notify slack')
parser.add_argument('--version', action='version',
                    version='Github PR Monitor ' + __version__)

log = logging.getLogger(__name__)
# Configuraiton is going to be global since this has been done in a functional manner instead of OO.
config = dict()


def setup_logging():
    """
    Configure logging.
    """
    log.setLevel(logging.DEBUG)
    console_out = logging.StreamHandler()
    console_out.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    console_out.setFormatter(formatter)
    log.addHandler(console_out)


def setup_vars():
    """
    Pull setup configuration from env vars.
    """
    if 'GH_API_TOKEN' in os.environ:
        config['githubtoken'] = os.getenv('GH_API_TOKEN')
    else:
        raise ValueError('GH_API_TOKEN is not set')

    if 'GH_REPO_NAME' in os.environ:
        config['gitrepo'] = os.getenv('GH_REPO_NAME')
    else:
        raise ValueError('GH_REPO_NAME is not set')

    if 'GH_OWNER' in os.environ:
        config['gitowner'] = os.getenv('GH_OWNER')
    else:
        raise ValueError('GH_OWNER is not set')

    if 'GH_PR_THRESH' in os.environ:
        config['agethreshold'] = os.getenv('GH_PR_THRESH')
    else:
        raise ValueError('GH_PR_THRESH is not set')

    if 'SLACK_HOOK' in os.environ:
        config['slackhook'] = os.getenv('SLACK_HOOK')
    else:
        raise ValueError('SLACK_HOOK is not set')
    try:
        requests.get(config['slackhook'])
    except requests.ConnectionError as exception:
        raise ValueError('Invalid URL - SLACK_HOOK is not a valid URL')

    if 'GH_PR_INTERVAL' in os.environ:
        config['interval'] = os.getenv('GH_PR_INTERVAL')
    else:
        config['interval'] = 300

    return config


def get_prs(client, gitowner, gitrepo):
    """
    Get the open Pull Requests.
    """
    repofetchname = gitowner + "/" + gitrepo
    try:
        repo = client.get_repo(repofetchname)
        pulls = repo.get_pulls('open')
    except client.GithubException.GithubException as e:
        print(f"Got an error: {e.status} {e.data}")
        logging.error(f'Error was reported with status {e.status} and data {e.data}')
    return pulls


def calculate_time_back(age):
    """
    Calculate Unix time back from age.
    """
    now = int(time.time())
    return now - age


def normalize_seconds(seconds: int) -> tuple:
    """
    Convert seconds to days hours minutes seconds.
    """
    (days, remainder) = divmod(seconds, 86400)
    (hours, remainder) = divmod(remainder, 3600)
    (minutes, seconds) = divmod(remainder, 60)

    return namedtuple("_", ("days", "hours", "minutes", "seconds"))(days, hours, minutes, seconds)


def notify_slack(pulls, color='red', owner='', repo='', webhook='', age=3600):
    """
    Make Slack notification to webhook.
    """
    if not webhook:
        raise Exception("Slack webhook is not configured")
    if not owner:
        raise Exception("Github owner is not configured")
    if not repo:
        raise Exception("Github repo is not configured")

    timetuple = normalize_seconds(int(age))
    agetext = str(timetuple.days) + ' days ' + str(timetuple.hours) + ' hours'
    payload = slack_payload(pulls, color, owner, repo, agetext)
    response = requests.post(
        webhook, data=json.dumps(payload),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )

    return 0


def slack_payload(pulls, color='red', owner='', repo='', agetext=''):
    """
    Build the JSON payload for Slack.
    """

    # Begin creating the JSON payload.
    j = defaultdict(lambda: defaultdict(list))
    j['blocks'] = []

    if color == 'red':
        icon = ':red_circle:'
        introtext = icon + ' There are ' + str(
            len(pulls)) + ' pull requests that need attention that are older than ' + agetext
    else:
        icon = ':green_apple:'
        introtext = icon + ' There are ' + str(len(pulls)) + ' open pull requests that are less than ' + agetext

    # Due to rate limits on slack, attempting to push information about every PR can go over rate limits on a
    # busy reop. It would take additional resources to post more information to Slack possibly including a Slack App.
    j['blocks'].append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": introtext
        }
    })
    return j


def job(argv=None):
    """
    Root job that is run by scheduler.
    """
    if argv is None:
        argv = sys.argv
    parser.parse_args(argv[1:])
    # Start logging.
    setup_logging()
    config = setup_vars()
    g = Github(config['githubtoken'])
    pullrequests = get_prs(g, config['gitowner'], config['gitrepo'])
    cutoff = calculate_time_back(int(config['agethreshold']))
    # Buckets of PR numbers.
    green = list()
    red = list()
    # Roll through the pull requests and sort into two buckets.
    for item in pullrequests:
        created = int(item.created_at.timestamp())
        url = item.html_url
        if created < cutoff:
            red.append(str(item.number))
        else:
            green.append(str(item.number))
    if len(red) > 0:
        notify_slack(red, 'red', config['gitowner'], config['gitrepo'], config['slackhook'], config['agethreshold'])
    if len(green) > 0:
        notify_slack(green, 'green', config['gitowner'], config['gitrepo'], config['slackhook'], config['agethreshold'])


def main():
    setup_vars()
    logging.basicConfig(level=logging.INFO)
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, 'interval', seconds=int(config['interval']))
    scheduler.start()
    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
