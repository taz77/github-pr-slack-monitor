[![Build Status](https://travis-ci.org/taz77/github-pr-slack-monitor.svg?branch=master)](https://travis-ci.org/taz77/github-pr-slack-monitor)

# Github PR Monitor Docker Service


## Building and Running Locally
A docker-compose.yml has been provided to allow for ease in building and running this app locally. An environment vairalbe file is used to run the container. Create a .env variable file
using the format described [here](https://docs.docker.com/compose/compose-file/#env_file).


## Environment Variables
| Variable Name  | Value  |
|---|---|
| GH_API_TOKEN | Github API Access Key  |
| GH_REPO_NAME  |  Name of the repository |
| GH_OWNER  | Repository owner (could be organization or name) |
| GH_PR_THRESH  | Threshold that can be set to flag Pull Requests as overdue in seconds |
|  SLACK_HOOK | Slack Webhook for your channel  |
| GH_PR_INTERVAL  | The interval at which to poll Github and report to Slack  |


## Base Image
We use the Python official base image that uses Alpine Linux.
