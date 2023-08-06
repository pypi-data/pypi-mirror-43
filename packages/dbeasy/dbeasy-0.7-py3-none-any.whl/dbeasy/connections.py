import json
from pathlib import Path

import sqlalchemy as sa
from sqlalchemy import engine


def get_sqlalchemy_engine(connection_name: str,
                          config_file: str or None = None,
                          **kwargs
                          ) -> engine.Engine:
    """
    Returns an sqlalchemy engine from a configuration file

    Args:
        connection_name: Name of connection in the configuration file
        config_file: Configuration file where the *connection_name* parameters are declared. Only JSON
        **kwargs: Additional parameters for sqlalchemy create_engine function
    Returns:
        A sqlalchemy engine
    """

    conf = load_connection_config(config_file, connection_name)

    # Check if connection configuration have all required variables
    _check_required_attrs(conf, connection_name)

    # Get connection configurations
    dialect = conf['dialect']
    driver = conf['driver']
    hostname = conf['host'] + ':' + conf['port'] if 'port' in conf else conf['host']
    user = conf['user']
    pwd = conf['pwd']
    database = conf['database']

    # Connection string
    cstr = '{}+{}://{}:{}@{}/{}'.format(dialect, driver, user, pwd, hostname, database)

    return sa.create_engine(cstr, **kwargs)


def load_connection_config(config_file, connection_name):
    # Loads the json data as dict
    filename = config_file if config_file is not None else str(Path.home()) + '/.dbconnections.json'
    with open(filename, 'r') as file:
        connections = json.load(file)
    # Check if connection name exists in configuration file
    if connection_name not in connections:
        raise ValueError("%s connection don't exists in %s" % (connection_name, filename))
    conf = connections[connection_name]
    return conf


def _check_required_attrs(connection_conf, connection_name):
    error_string = 'Required Attribute %s not declared in configuration file for connection %s.'
    required_attr = ('dialect', 'driver', 'user', 'pwd', 'host', 'database')
    for v in required_attr:
        if v not in connection_conf:
            raise RuntimeError(error_string % (v, connection_name))


# Defines only if ctds exists
try:
    import ctds
except:
    pass
else:
    def get_ctds_connection(connection_name: str, config_file: str = None) -> ctds.Connection:
        """
        Create a ctds connection from a connection define in a json file
        Args:
            connection_name: Name of connection
            config_file: Name of file with defined connections
        Returns:
            ctds.Connection: A ctds connection
        """
        conf: dict = load_connection_config(config_file, connection_name)

        if conf['dialect'] != 'mssql':
            raise RuntimeError('%s is not a MSSQL connection.' % connection_name)

        hostname: str = conf['host']
        port: int = int(conf.get('port', '1433'))
        user: str = conf['user']
        pwd: str = conf['pwd']
        database: str = conf['database']

        conn = ctds.connect(hostname, port, user=user, password=pwd, database=database, login_timeout=300, timeout=300)
        return conn
