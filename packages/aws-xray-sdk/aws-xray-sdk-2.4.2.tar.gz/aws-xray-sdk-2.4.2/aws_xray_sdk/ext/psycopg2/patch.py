import copy
import re
import wrapt
from operator import methodcaller

from aws_xray_sdk.ext.dbapi2 import XRayTracedConn, XRayTracedCursor


def patch():

    wrapt.wrap_function_wrapper(
        'psycopg2',
        'connect',
        _xray_traced_connect
    )
    wrapt.wrap_function_wrapper(
        'psycopg2.extensions',
        'register_type',
        _xray_register_type_fix
    )


def _xray_traced_connect(wrapped, instance, args, kwargs):

    conn = wrapped(*args, **kwargs)
    parameterized_dsn = { c[0]: c[-1] for c in map(methodcaller('split', '='), conn.dsn.split(' '))}
    meta = {
        'database_type': 'PostgreSQL',
        'url': 'postgresql://{}@{}:{}/{}'.format(
            parameterized_dsn.get('user', 'unknown'),
            parameterized_dsn.get('host', 'unknown'),
            parameterized_dsn.get('port', 'unknown'),
            parameterized_dsn.get('dbname', 'unknown'),
        ),
        'user': parameterized_dsn.get('user', 'unknown'),
        'database_version': str(conn.server_version),
        'driver_version': 'Psycopg 2'
    }

    return XRayTracedConn(conn, meta)

def _xray_register_type_fix(wrapped, instance, args, kwargs):
    """Send the actual connection or curser to register type."""
    our_args = list(copy.copy(args))
    if len(our_args) == 2 and isinstance(our_args[1], (XRayTracedConn, XRayTracedCursor)):
        our_args[1] = our_args[1].__wrapped__

    return wrapped(*our_args, **kwargs)
