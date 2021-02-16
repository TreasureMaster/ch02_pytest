"""Проверка на ожидаемые исключения из-за неправильного использования API."""

import pytest
import tasks
from tasks import Task


def test_add_raises():
    """add() должно возникнуть исключение с неправильным типом param."""
    # pytest.raises сообщает, что все, что находиться в следующем блоке кода
    # должно вызывать исключение TypeError
    with pytest.raises(TypeError):
        tasks.add(task='not a Task object')


def test_start_tasks_db_raises():
    """Убедитесь, что не поддерживаемая БД вызывает исключение."""
    # Также можно проверить параметры исключения
    with pytest.raises(ValueError) as excinfo:
        tasks.start_tasks_db('some/great/path', 'mysql')
    exception_msg = excinfo.value.args[0]
    assert exception_msg == "db_type must be a 'tiny' or 'mongo'"


# pytest -m "smoke" test_api_exceptions.py выберет тесты с маркером smoke
# pytest -m "smoke and not get" test_api_exceptions.py выберет тесты с маркером smoke, но в котором нет маркера get
@pytest.mark.smoke
def test_list_raises():
    """list() должно возникнуть исключение с неправильным типом param."""
    with pytest.raises(TypeError):
        tasks.list_tasks(owner=123)


@pytest.mark.get
@pytest.mark.smoke
def test_get_raises():
    """get() должно возникнуть исключение с неправильным типом param."""
    with pytest.raises(TypeError):
        tasks.get(task_id='123')


class TestUpdate():
    """Тест ожидаемых исключений с tasks.update()."""

    def test_bad_id(self):
        """non-int id должен поднять exception."""
        with pytest.raises(TypeError):
            tasks.update(task_id={'dict instead': 1}, task=tasks.Task())

    def test_bad_task(self):
        """non-Task задача должна поднять exception."""
        with pytest.raises(TypeError):
            tasks.update(task_id=1, task='not a task')


@pytest.mark.usefixtures('tasks_db')
class TestAdd():
    """Тесты, связанные с tasks.add()."""

    def test_missing_summary(self):
        """Следует поднять исключение, если параметр summary отсутсвует."""
        with pytest.raises(ValueError):
            tasks.add(Task(owner='bob'))

    def test_done_not_bool(self):
        """Должно вызвать исключение, если done не является bool."""
        with pytest.raises(ValueError):
            tasks.add(Task(summary='summary', done='True'))