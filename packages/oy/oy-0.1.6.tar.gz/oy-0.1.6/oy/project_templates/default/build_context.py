# -*-coding: utf-8-*-

# This file is used to generate the render context to
# be used in the rendering of other files in this project
# It will be deleted from the final output folder

import secrets
import oy

__all__ = ["secret_key", "db_uri", "password_sult", "oy_version"]


secret_key = secrets.token_hex(32)
db_uri = "db.sqlite"
password_sult = secrets.token_hex(32)
oy_version = oy.__version__
