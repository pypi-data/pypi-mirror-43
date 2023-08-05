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

import abc


class FetcherBase(metaclass=abc.ABCMeta):
    """A base class for implementing per-ecosystem specific digest fetchers."""

    @abc.abstractmethod
    def fetch(self, package_name: str, package_version: str) -> dict:
        """Fetch digests of files specific for the given package in its version."""
        raise NotImplementedError
