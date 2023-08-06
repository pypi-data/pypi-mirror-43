"""LICENSE
Copyright 2019 Hermann Krumrey <hermann@krumreyh.com>

This file is part of status-page.

status-page is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

status-page is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with status-page.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""

from typing import Dict, Any
from status_page.analytics.ping import port_ping, ping
from status_page.analytics.version import get_gitlab_version, \
    get_version_from_version_file
from status_page.analytics.web import test_webpage


def generate_analytics_data(server_list_config: Dict[str, Dict[str, Any]]) \
        -> Dict[str, Dict[str, Any]]:
    """
    Analyzes the servers provided as argument and generates a dictionary
    containing data which can be visualized.
    :param server_list_config: The config to analyze
    :return: The analyzed data
    """
    analyzed = {}

    for server in sorted(server_list_config):
        server_config = server_list_config[server]

        is_up = True
        _version = None

        address = server_config["address"]
        port = server_config.get("port")
        gitlab_api_token = server_config.get("gitlab-api-token")
        version_file = server_config.get("version-file")

        for action in server_config["actions"]:

            if action == "ping":
                is_up = is_up and ping(address)

            elif action == "port_ping":
                is_up = is_up and port_ping(address, port)

            elif action == "gitlab-version":
                _version = get_gitlab_version(address, gitlab_api_token)

            elif action == "version-file":
                _version = get_version_from_version_file(version_file)

            elif action == "web":
                is_up = is_up and test_webpage(address)

        analyzed[server] = {
            "is_up": is_up,
            "version": _version
        }

    return analyzed
