"""Handle configuration files for tasks CLI."""

import sys
from collections import namedtuple
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser
import os


TasksConfig = namedtuple('TasksConfig', ['db_path', 'db_type'])


def get_config():
    """Return TasksConfig object after reading config file."""
    parser = ConfigParser()
    if sys.platform.startswith('win'):
        config_line = '~/tests/config.ini'
    else:
        config_line = '~/.tasks.config'
    config_file = os.path.normpath(os.path.expanduser(config_line))
    if not os.path.exists(config_file):
        tasks_db_path = '~/tests/tasks_db/'
        tasks_db_type = 'tiny'
    else:
        parser.read(config_file)
        tasks_db_path = parser.get('TASKS', 'tasks_db_path')
        tasks_db_type = parser.get('TASKS', 'tasks_db_type')
    tasks_db_path = os.path.normpath(os.path.expanduser(tasks_db_path))
    return TasksConfig(tasks_db_path, tasks_db_type)


if __name__ == '__main__':
    # Данный блок предусмотрен для изучения configparser
    print(os.path.normpath(os.path.expanduser('~/.tasks.config')))
    print(get_config())