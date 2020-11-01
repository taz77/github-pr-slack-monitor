#!/usr/bin/env python
import argparse
import sys
import os
from .jsonreader import JsonReader
import json
from mako.template import Template
from mako import exceptions


def get_vars():
    # Get the ENV var that determins what ENV we are working wtih
    if 'DEPLOY_ENV' in os.environ:
        depenv = os.getenv('DEPLOY_ENV')
    else:
        raise ValueError('DEPLOY_ENV is not set')

    # Read the appropriate json file for the env
    jsonread = JsonReader()
    config = jsonread.json_to_read(depenv)

    if 'GH_API_TOKEN' in os.environ:
        config['gh_api_token'] = os.getenv('GH_API_TOKEN')
    else:
        raise ValueError('GH_API_TOKEN is not set')

    if 'GH_REPO_NAME' in os.environ:
        config['gh_repo_name'] = os.getenv('GH_REPO_NAME')
    else:
        raise ValueError('GH_REPO_NAME is not set')

    if 'GH_OWNER' in os.environ:
        config['gh_owner'] = os.getenv('GH_OWNER')
    else:
        raise ValueError('GH_OWNER is not set')

    if 'GH_PR_THRESH' in os.environ:
        config['gh_pr_thresh'] = os.getenv('GH_PR_THRESH')
    else:
        raise ValueError('GH_PR_THRESH is not set')

    if 'SLACK_HOOK' in os.environ:
        config['slack_hook'] = os.getenv('SLACK_HOOK')
    else:
        raise ValueError('SLACK_HOOK is not set')

    if 'GH_PR_INTERVAL' in os.environ:
        config['gh_pr_interval'] = os.getenv('GH_PR_INTERVAL')
    else:
        config['gh_pr_interval'] = 300

    if 'GH_PR_TAG' in os.environ:
        config['tag'] = os.getenv('GH_PR_TAG')
    else:
        config['tag'] = 'latest'

    return config

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', help="Output file",
                        dest='output', type=argparse.FileType('w'))
    parser.parse_args()
    args = parser.parse_args(argv)
    tempvars = get_vars()
    try:
        template = Template(filename='compose.yml.tpl')
        deployment = template.render(**tempvars)
    except:
        print(exceptions.text_error_template().render())
    outfile = args.output
    outfile.write(deployment)
    outfile.close()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
