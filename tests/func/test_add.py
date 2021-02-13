"""Проверьте функцию API tasks.add()."""

import pytest
import tasks
from tasks import Task

# WARNING Если есть pyproject.toml, то настройки pytest нужно перенести в него из pytest.ini

def test_add_returns_valid_id():
    """tasks.add(valid task) должен возвращать целое число."""
    # ДАЕТ инициализированные задачи db
    # КОГДА добавляется новая задача
    # ТОГДА возвращаемый task_id имеет тип int
    new_task = Task('do something')
    task_id = tasks.add(new_task)
    assert isinstance(task_id, int)


@pytest.mark.smoke
def test_added_task_has_id_set():
    """Убедимся, что поле task_id установлено tasks.add()."""
    # ДАЕТ инициализированные задачи db
    # И добавлена новая задача
    new_task = Task('sit in chair', owner='me', done=True)
    task_id = tasks.add(new_task)

    # КОГДА задача получена
    task_from_db = tasks.get(task_id)

    # ТОГДА task_id соответствует полю id
    assert task_from_db.id == task_id


# Параметр autouse показывает, что все тесты в этом файле будут использовать данную fixture
@pytest.fixture(autouse=True)
def initialized_tasks_db(tmpdir):
    """Соединение с БД перед тестом, разъединение после."""
    # Инициализация: старт БД
    tasks.start_tasks_db(str(tmpdir), 'tiny')
    # здесь происходит тестирование
    yield
    # После тестов: стоп БД
    tasks.stop_tasks_db()