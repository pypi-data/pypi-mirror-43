__version__ = "1.1.0"

import os

from .config import Config, normalize_app_name
from .logging import Logger

config = None
logger = None
APP_ENV_NAME = None
TRUE_VALUES = {"true", "1"}


def start(
    name,
    project_config_dir=None,
    test=False,
    debug=True,
    paths=None,
    byte_units=None,
    second_units=None,
    without_daiquiri=None,
):
    global config, logger, APP_ENV_NAME, TRUE_VALUES

    APP_ENV_NAME = normalize_app_name(name)
    if without_daiquiri is None:
        without_daiquiri = (
            os.getenv("{}_NO_DAIQUIRI".format(APP_ENV_NAME)) in TRUE_VALUES
        )

    config = Config(
        name,
        project_config_dir=project_config_dir,
        test=test,
        debug=debug,
        paths=paths,
        byte_units=byte_units,
        second_units=second_units,
    )
    logger = Logger(name, without_daiquiri=without_daiquiri)
