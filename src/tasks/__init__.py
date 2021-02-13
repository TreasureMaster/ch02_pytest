"""Minimal Project Task Management."""

from .api import (  # noqa: F401
    Task,
    TasksException,
    add,
    get,
    list_tasks,
    count,
    update,
    delete,
    delete_all,
    unique_id,
    start_tasks_db,
    stop_tasks_db
)

from pkg_resources import get_distribution


__version__ = get_distribution('tasks').version