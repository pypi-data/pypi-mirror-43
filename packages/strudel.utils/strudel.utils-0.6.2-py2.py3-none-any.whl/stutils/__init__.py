
"""

"""

import os

try:
    import settings
except ImportError:
    settings = object()

__version__ = '0.6.2'
__author__ = "Marat (@cmu.edu)"
__license__ = "GPL v3"

CONFIG = {}


def get_config(variable, default=None):
    """ Get configuration variable for strudel.* packages

    Args:
        variable (str): name of the config variable
        default: value to use of config variable not set

    Returns:
        variable value

    Order of search:
        1. stutils.CONFIG
        2. settings.py of the current folder
        3. environment variable

    Known config vars so far:
        strudel.utils
        ST_FS_CACHE_DURATION - duration of filesystem cache in seconds
        ST_FS_CACHE_PATH - path to the folder to store filesystem cache

        strudel.ecosystems
        PYPI_SAVE_PATH - place to store downloaded PyPI packages
        PYPI_TIMEOUT - network timeout for PyPI API

        strudel.scraper
        GITHUB_API_TOKENS - comma separated list of GitHub tokens
        GITLAB_API_TOKENS - same for GitLab API
    """
    if variable in CONFIG:
        return CONFIG[variable]

    if hasattr(settings, variable):
        return getattr(settings, variable)

    if variable in os.environ:
        return os.environ[variable]

    return default


def set_config(variable, value):
    """ Set configuration variable globally for all strudel.* packages """
    CONFIG[variable] = value
