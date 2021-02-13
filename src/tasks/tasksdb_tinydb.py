"""Database wrapper for TinyDB for tasks project."""

import tinydb
import os
from typing import Optional, List


class TasksDB_TinyDB():     # noqa: E801
    """Wrapper class for TinyDB.

    The methods in this class need to match
    all database interaction classes.

    So far, this is:
    TasksDB_MongoDB found in tasksdb_pymongo.py.
    TasksDB_TinyDB found in tasksdb_tinydb.py.
    """

    def __init__(self, db_path: str) -> None:
        """Connect to db."""
        self._db = tinydb.TinyDB(os.path.normpath(db_path + '/tasks_db.json'))

    def add(self, task: dict) -> int:
        """Add a task dict to db."""
        task_id = self._db.insert(task)
        task['id'] = task_id
        self._db.update(task, doc_ids=[task_id])
        return task_id

    def get(self, task_id: int) -> dict:
        """Return a task dict with matching id."""
        return self._db.get(doc_id=task_id)

    def list_tasks(self, owner: Optional[str]=None) -> List[dict]:
        """Return list of tasks."""
        if owner is None:
            return self._db.all()
        else:
            return self._db.search(tinydb.Query().owner == owner)

    def count(self) -> int:
        """Return number of tasks in db."""
        return len(self._db)

    def update(self, task_id: int, task: dict) -> None:
        """Modify task in db with given task_id."""
        self._db.update(task, doc_ids=[task_id])

    def delete(self, task_id: int) -> None:
        """Remove a task from db with given task_id."""
        self._db.remove(doc_ids=[task_id])

    def delete_all(self) -> None:
        """Remove all tasks from db."""
        self._db.purge()

    def unique_id(self) -> int:
        """Return an integer that does not exist in the db."""
        i = 1
        while self._db.contains(doc_ids=[i]):
            i += 1
        return i

    def stop_tasks_db(self) -> None:
        """Disconnect from db."""
        self._db.close()


def start_tasks_db(db_path: str) -> TasksDB_TinyDB:
    """Connect to db."""
    return TasksDB_TinyDB(db_path)