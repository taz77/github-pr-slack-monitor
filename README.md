# Github PR Monitor Docker Service

Fork, clone, or copy this repository to start your Docker Python application.

# Running
The python application is contained in the `app` folder. [Setuptools](https://setuptools.readthedocs.io/en/latest/) is used to install and manage dependencies. 


# Installation
We use Setuptools configuration file to control requirements. In this example there are extra requirements for devleopment that includes pandas. Installation is done via:

```pip install -e .[dev]```

# Base Image
We use the Python official base image that uses Alpine Linux.
