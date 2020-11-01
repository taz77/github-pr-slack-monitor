# Deployment Helper

Python package to dynamically create configurations from a template file for deployment pipelines.

## Usage
The app takes a single arguement to create the rendered file. Pass either `-o` or `--output` and the filename.
Example:

  `app.py -o filename.yml`


The compose.yml.tpl can be changed for different deployment environments.

## Environment Variables

The configuration of the template file is controlled by environment variables that should come from a secrets store..

| Variable Name  | Value  |
|---|---|
| DEPLOY_ENV  | The environment the deployment is going into |
| GH_API_TOKEN | Github API Access Key  |
| GH_REPO_NAME  |  Name of the repository |
| GH_OWNER  | Repository owner (could be organization or name) |
| GH_PR_THRESH  | Threshold that can be set to flag Pull Requests as overdue in seconds |
|  SLACK_HOOK | Slack Webhook for your channel  |
| GH_PR_INTERVAL  | The interval at which to poll Github and report to Slack  |
| GH_PR_TAG | The tag for the container being deployed |

