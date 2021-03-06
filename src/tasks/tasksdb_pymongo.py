"""Database wrapper for MongoDB for tasks project."""

import os
import pymongo
import subprocess
import time
from bson.objectid import ObjectId
from typing import Optional, List


class TasksDB_MongoDB():    # noqa: E801
    """Wrapper class for MongoDB.

    The methods in this class need to match
    all database interaction classes.

    So far, this is:
    TasksDB_TinyDB found in tasksdb_tinydb.py.
    """

    def __init__(self, db_path: str) -> None:
        """Start MongoDB client and connect to db."""
        self._process = None
        self._client = None
        # Старт сервера MongoDB и определение процесса self._process
        self._start_mongod(db_path)
        # Соединение с БД, создание БД и пользовательского счетчика
        self._connect()

    def add(self, task: dict) -> int:
        """Add a task dict to db."""
        task['_id'] = self._get_next_task_id()
        return self._db.task_list.insert_one(task).inserted_id

    def get(self, task_id: int) -> dict:
        """Return a task dict with matching id."""
        task_dict = self._db.task_list.find_one({'_id': task_id})
        task_dict['id'] = task_dict.pop('_id')
        return task_dict

    def list_tasks(self, owner: Optional[str]=None) -> List[dict]:
        """Return list of tasks."""
        if owner is None:
            all = self._db.task_list.find()
        else:
            all = self._db.task_list.find({'owner': owner})
        all = list(all)
        # WARNING all - это итератор, тут он опустошается
        for task_dict in all:
            task_dict['id'] = task_dict.pop('_id')
        return all

    def count(self) -> int:
        """Return number of tasks in db."""
        return self._db.task_list.estimated_document_count()

    def last_id(self) -> int:
        """Return last id from db."""
        if self.count():
            return self._db.task_list.find_one(sort=[('_id', -1)])['_id']
        return self.count()

    def update(self, task_id: int, task: dict) -> None:
        """Modify task in db with given task_id."""
        self._db.task_list.find_one_and_update({'_id': task_id}, {'$set': task})

    def delete(self, task_id: int) -> None:
        """Remove a task from db with given task_id."""
        reply = self._db.task_list.delete_one({'_id': task_id})
        if reply.deleted_count == 0:
            raise ValueError('id {} not in task database'.format(str(task_id)))

    def unique_id(self) -> int:
        """Return an integer that does not exist in the db."""
        tail_task_ids = self._db.counters.find_one({'_id': 'tasksid'})
        uid = tail_task_ids['seq'] + 1
        return uid

    def delete_all(self) -> None:
        """Remove all tasks from db."""
        self._db.task_list.drop()

    def stop_tasks_db(self) -> None:
        """Disconnect from db."""
        self._disconnect()
        self._stop_mongod()

    def _start_mongod(self, db_path: str) -> None:
        """Старт сервера mongod в отдельном процессе."""
        self._devnull = open(os.devnull, 'wb')
        self._process = subprocess.Popen(
            ['mongod', '--dbpath', db_path],
            stdout=self._devnull,
            stderr=subprocess.STDOUT
        )
        assert self._process, 'mongod process failed to start'

    def _stop_mongod(self) -> None:
        if self._client:
            self._client = None
        if self._process:
            self._process.terminate()
            self._process.wait()
            self._devnull.close()
            self._process = None

    def _connect(self) -> None:
        if self._process and (not self._client or not self._db):
            for _ in range(3):
                try:
                    # соединение с БД
                    self._client = pymongo.MongoClient()
                except pymongo.errors.ConnectionFailure:
                    time.sleep(0.1)
                    continue
                else:
                    break
            if self._client:
                # создание БД task_db
                self._db = self._client.task_db
                # создание идентификатора tasksid, начинающегося с 0, в коллекции counters (специальной ?)
                # WARNING вероятно, pymongo где-то создает _id: 1 (можно ли его сбросить ?)
                # ANSWER вроде сработало! Просто заменяем встроенный _id своим.
                # self._db.counters.insert_one({'_id': 'tasksid', 'seq': 0})
                # self._reset_task_id()
                self._set_last_field()

    def _reset_task_id(self) -> None:
        self._db.counters.find_one_and_update({'_id': 'tasksid'},
                                              {'$set': {'seq': 0}})

    def _set_last_field(self) -> None:
        self._db.counters.find_one_and_update({'_id': 'tasksid'},
                                              {'$set': {'seq': self.last_id()}})

    def _get_next_task_id(self):
        ret = self._db.counters.find_one_and_update({'_id': 'tasksid'},
                                                    {'$inc': {'seq': 1}},
                                                    return_document=pymongo.ReturnDocument.AFTER)
        return ret['seq']

    def _disconnect(self) -> None:
        self._db = None


def start_tasks_db(db_path: str) -> TasksDB_MongoDB:
    """Connect to db."""
    return TasksDB_MongoDB(db_path)


if __name__ == '__main__':
    from tasks import Task
    task = start_tasks_db('C:\\Users\\DEUS\\tests\\mongo_db')
    print('id на старте (указатель):', task.last_id())
    # Вставляем 3 записи
    print('1-e add:', task.add(Task('do something great')._asdict()))
    print('last id:', task.last_id())
    print('2-e add:', task.add(Task('repeat', owner='Brian')._asdict()))
    print('last id:', task.last_id())
    print('3-e add:', task.add(Task('again and again', owner='Okken')._asdict()))
    print('last id:', task.last_id())
    # Вставляем 4-ю запись
    task_id = (task.add(Task('testing', owner='Brian')._asdict()))
    print('get id=last:', task.get(task.last_id()))
    print('count:', task.count())
    print('Все записи:')
    for entry in task.list_tasks():
        print(entry)
    print('-'*40)
    print('list_tasks(Brian):', task.list_tasks('Brian'))
    task.delete(task.last_id())
    print('count:', task.count())
    print('После удаления последней записи:')
    for entry in task.list_tasks():
        print(entry)
    print('-'*40)
    id2 = Task('again and again +', owner='Okken', done=True)._asdict()
    print('task для update:', id2)
    task.update(task.last_id(), id2)
    print('get id=last after update:', task.get(task.last_id()))
    print('count:', task.count())
    print('-'*40)
    for entry in task.list_tasks():
        print(entry)
    task.delete_all()
    task.stop_tasks_db()