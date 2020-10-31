# Github PR Monitor Docker Service

Fork, clone, or copy this repository to start your Docker Python application.

# Running
The python application is contained in the `app` folder. [Setuptools](https://setuptools.readthedocs.io/en/latest/) is used to install and manage dependencies. 


# Installation
We use Setuptools configuration file to control requirements. In this example there are extra requirements for devleopment that includes pandas. Installation is done via:

```pip install -e .[dev]```


# Environment Variables
| Variable Name  | Value  |
|---|---|
| GH_API_TOKEN | Github API Access Key  |
| GH_REPO_NAME  |  Name of the repository |
| GH_OWNER  | Repository owner (could be organization or name) |
| GH_PR_THRESH  | Threshold that can be set to flag Pull Requests as overdue in seconds |
|  SLACK_HOOK | Slack Webhook for your channel  |
| GH_PR_INTERVAL  | The interval at which to poll Github and report to Slack  |




# Base Image
We use the Python official base image that uses Alpine Linux.
