#!/usr/bin/env python3
# thoth-digests-fetcher
# Copyright(C) 2019 ???
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""A command line interface for Python digests fetcher used in project Thoth."""

import logging

import click
from thoth.common import init_logging
from thoth.analyzer import print_command_result
from thoth.digests_fetcher import __version__ as analyzer_version
from thoth.digests_fetcher import __title__ as analyzer_name
from thoth.digests_fetcher.python import PythonDigestsFetcher


init_logging()
_LOGGER = logging.getLogger(__name__)


def _print_version(ctx, _, value):
    """Print adviser version and exit."""
    if not value or ctx.resilient_parsing:
        return
    click.echo(analyzer_version)
    ctx.exit()


@click.group()
@click.pass_context
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    envvar="THOTH_DIGESTS_FETCHER_DEBUG",
    help="Be verbose about what's going on.",
)
@click.option(
    "--version",
    is_flag=True,
    is_eager=True,
    callback=_print_version,
    expose_value=False,
    help="Print digests fetcher version and exit.",
)
def cli(ctx=None, verbose=False):
    """Thoth's digests-fetcher command line interface."""
    if ctx:
        ctx.auto_envvar_prefix = "THOTH_DIGESTS_FETCHER"

    if verbose:
        _LOGGER.setLevel(logging.DEBUG)

    _LOGGER.debug("Debug mode is on")
    _LOGGER.info("Version: %s", analyzer_version)


@cli.command()
@click.pass_context
@click.option(
    "--package-name",
    "-p",
    type=str,
    required=True,
    envvar="THOTH_DIGESTS_FETCHER_PACKAGE_NAME",
    help="Package name for which digests should be fetcher.",
)
@click.option(
    "--package-version",
    "-v",
    type=str,
    required=True,
    envvar="THOTH_DIGESTS_FETCHER_PACKAGE_VERSION",
    help="Package name for which digests should be fetcher.",
)
@click.option(
    "--index-url",
    "-i",
    type=str,
    required=False,
    default="https://pypi.org/simple",
    show_default=True,
    envvar="THOTH_DIGESTS_FETCHER_INDEX_URL",
    help="A comma separated list of Python package indexes (package sources) to gather digests from.",
)
@click.option("--no-pretty", "-P", is_flag=True, help="Do not print results nicely.")
def python(
    click_ctx,
    package_name: str,
    package_version: str,
    index_url: str = None,
    no_pretty: bool = True,
    output: str = None,
):
    """Fetch digests for packages in Python ecosystem."""
    result = {}
    for url in index_url.split(","):
        python_fetcher = PythonDigestsFetcher(url)
        result[url] = python_fetcher.fetch(package_name, package_version)

    print_command_result(
        click_ctx,
        result,
        analyzer=analyzer_name,
        analyzer_version=analyzer_version,
        output=output,
        pretty=not no_pretty,
    )


if __name__ == "__main__":
    cli()
