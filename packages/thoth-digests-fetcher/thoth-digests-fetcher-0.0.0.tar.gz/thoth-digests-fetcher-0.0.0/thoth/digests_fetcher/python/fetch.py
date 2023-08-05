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

"""Fetch digests for packages in Python ecosystem."""

import logging

from thoth.python import Source
from thoth.digests_fetcher.base import FetcherBase

_LOGGER = logging.getLogger(__name__)


class PythonDigestsFetcher(FetcherBase):
    """Fetch digests of python package artifacts and all the files present in artifacts."""

    def __init__(self, index_url: str):
        """Initialize Python digests fetcher."""
        self.source = Source(index_url)

    def fetch(self, package_name: str, package_version: str) -> dict:
        """Fetch digests of files present in artifacts for the given package."""
        _LOGGER.info(
            "Fetching digests for package %r in version %r from %r",
            package_name,
            package_version,
            self.source.url,
        )

        # TODO: implement
        return {
            "package_name": package_name,
            "package_version": package_version,
            "index_url": self.source.index.url,
            "files": [],
        }
