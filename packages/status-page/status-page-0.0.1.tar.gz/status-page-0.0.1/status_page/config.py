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

import os
from status_page.utils.env import resolve_env_variable, load_secrets

"""
This file contains environment specific configuration information
All of this information is found using environment variables
"""

secrets_file = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    "../secrets.json"
)
if os.path.isfile(secrets_file):
    load_secrets(secrets_file)


smtp_address = resolve_env_variable(
    "SMTP_ADDRESS", default="noreply@status_page.namibsun.net"
)
"""
The SMTP username used for sending emails
"""

smtp_server = resolve_env_variable("SMTP_SERVER", default="smtp.strato.de")
"""
The SMTP server used for sending emails
"""

smtp_port = resolve_env_variable("SMTP_PORT", int, default=587)
"""
The SMTP server port used for sending emails
"""

smtp_password = resolve_env_variable("SMTP_PASSWORD")
"""
The password of the SMTP account
"""

db_user = resolve_env_variable("DB_USER")
"""
The database user
"""

db_name = resolve_env_variable("DB_NAME")
"""
The database name
"""

db_key = resolve_env_variable("DB_KEY")
"""
The database key
"""

logging_path = os.path.join(
    str(resolve_env_variable("PROJECT_ROOT_PATH", default="/tmp")),
    "status_page.log"
)
