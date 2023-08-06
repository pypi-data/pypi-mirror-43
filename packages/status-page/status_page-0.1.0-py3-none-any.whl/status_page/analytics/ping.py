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

from subprocess import check_output, check_call, CalledProcessError


def ping(address: str) -> bool:
    """
    Pings an address and checks whether or not the address responds
    :param address: The address to ping
    :return: Whether or not the device responds to the ping
    """
    try:
        status = check_call(["ping", "-c", "1", "-w", "1", address])
        return status == 0
    except CalledProcessError:
        return False


def port_ping(address: str, port: int) -> bool:
    """
    Pings an address at a specific port using nmap and checks whether or not
    the address responds
    :param address: The address to ping
    :param port: The port to ping
    :return: Whether or not the device responds to the ping
    """
    try:
        response = check_output(["nmap", "-p", str(port), address])
        return "open" in response.decode("utf-8")
    except CalledProcessError:
        return False
