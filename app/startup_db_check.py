"""
Runs once before the web server starts.

Makes a single attempt to reach the database. If the database is not accepting
connections yet, this exits non-zero and takes the container down with it.

That is deliberate. There is no retry loop here on purpose: the point of this
lab is that startup ordering is the orchestrator's job, not something every
service should have to paper over by itself.
"""

import sys

from db import get_db_connection

try:
    connection = get_db_connection()
    connection.close()
    print("startup check: database is reachable")
except Exception as error:
    print(f"startup check FAILED: cannot reach the database -- {error}")
    sys.exit(1)
