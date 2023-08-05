#!/usr/bin/env python3
import logging
import os
from distutils.util import strtobool

import click

from r2c.cli.core import cli
from r2c.cli.errors import CliError

logger = logging.getLogger(__name__)


def is_debug_mode() -> bool:
    return strtobool(os.getenv("DEBUG", "False"))


if __name__ == "__main__":
    try:
        cli(obj={}, prog_name="r2c")
    except CliError as ce:
        if is_debug_mode():
            logger.exception(ce)
        click.echo(
            f"❌ {ce}. Please use `r2c --debug <CMD>`, to get stack trace. For more help, reach out to R2C  at support@ret2.co"
        )
    except Exception as e:
        if is_debug_mode():
            logger.exception(e)
        else:
            click.echo(
                f"❌ Unexpected error. Please run `r2c --debug <CMD>` to get more detailed information. Contact us for more help."
            )
