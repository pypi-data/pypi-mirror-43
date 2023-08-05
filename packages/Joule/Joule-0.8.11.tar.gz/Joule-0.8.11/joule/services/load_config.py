import os
import configparser
import ipaddress
import requests
import psycopg2

from joule.models import config
from joule.errors import ConfigurationError

"""
[Main]
  ModuleDirectory = /etc/joule/module_configs
  StreamDirectory = /etc/joule/stream_configs
  IPAddress = 127.0.0.1
  Port = 8088
  Database = joule:joule@localhost:5432/joule
  InsertPeriod = 5
  CleanupPeriod = 60
  MaxLogLines = 100
  NilmdbUrl = http://localhost/nilmdb
"""
def run(custom_values=None, verify=True) -> config.JouleConfig:
    """provide a dict INI configuration to override defaults
       if verify is True, perform checks on settings to make sure they are appropriate"""
    my_configs = configparser.ConfigParser()
    my_configs.read_dict(config.DEFAULT_CONFIG)
    if custom_values is not None:
        my_configs.read_dict(custom_values)

    main_config = my_configs['Main']
    # ModuleDirectory
    module_directory = main_config['ModuleDirectory']
    if not os.path.isdir(module_directory) and verify:
        raise ConfigurationError(
            "ModuleDirectory [%s] does not exist" % module_directory)
    # StreamDirectory
    stream_directory = main_config['StreamDirectory']
    if not os.path.isdir(stream_directory) and verify:
        raise ConfigurationError(
            "StreamDirectory [%s] does not exist" % stream_directory)
    # IPAddress
    ip_address = main_config['IPAddress']
    try:
        ipaddress.ip_address(ip_address)
    except ValueError as e:
        raise ConfigurationError("IPAddress is invalid") from e
    # Port
    try:
        port = int(main_config['Port'])
        if port < 0 or port > 65535:
            raise ValueError()
    except ValueError as e:
        raise ConfigurationError("Port must be between 0 - 65535") from e

    # Nilmdb URL
    if 'NilmdbUrl' in main_config and main_config['NilmdbUrl'] != '':
        nilmdb_url = main_config['NilmdbUrl']
        if verify:
            try:
                resp = requests.get(nilmdb_url)
                if not resp.ok:
                    raise requests.exceptions.ConnectionError
            except requests.exceptions.ConnectionError:
                raise ConfigurationError(
                    "Cannot contact NilmDB server at [%s]" % nilmdb_url
                )
            if 'NilmDB' not in resp.text:
                raise ConfigurationError(
                    "Host at [%s] is not a NilmDB server" % nilmdb_url
                )
    else:
        nilmdb_url = None

    # Database
    if 'Database' in main_config:
        database = "postgresql://"+main_config['Database']
    elif verify:
        raise ConfigurationError("Missing [Database] configuration")
    else:  # pragma: no cover
        database = ''  # this is invalid of course, just used in unit testing
    if verify:
        # check to see if this is a valid database DSN
        try:
            conn = psycopg2.connect(database)
            conn.close()
        except psycopg2.Error:
            raise ConfigurationError("Cannot connect to database [%s]" % database)

    # InsertPeriod
    try:
        insert_period = int(main_config['InsertPeriod'])
        if insert_period <= 0:
            raise ValueError()
    except ValueError:
        raise ConfigurationError("InsertPeriod must be a postive number")

    # CleanupPeriod
    try:
        cleanup_period = int(main_config['CleanupPeriod'])
        if cleanup_period <= 0 or cleanup_period < insert_period:
            raise ValueError()
    except ValueError:
        raise ConfigurationError("CleanupPeriod must be a postive number > InsertPeriod")

    # Max Log Lines
    try:
        max_log_lines = int(main_config['MaxLogLines'])
        if max_log_lines <= 0:
            raise ValueError()
    except ValueError:
        raise ConfigurationError("MaxLogLines must be a postive number")

    return config.JouleConfig(module_directory=module_directory,
                              stream_directory=stream_directory,
                              ip_address=ip_address,
                              port=port,
                              database=database,
                              insert_period=insert_period,
                              cleanup_period=cleanup_period,
                              max_log_lines=max_log_lines,
                              nilmdb_url=nilmdb_url
                              )
