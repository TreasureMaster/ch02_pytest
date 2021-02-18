"""Тест tasks.unique_id()."""

import pytest
import tasks
from tasks.api import Task


# WARNING данный код вызывает обрушение тестов, т.к. подавляет действие conftest.py
# @pytest.fixture(autouse=True)
# def initialized_tasks_db(tmpdir):
#     """Соединение с БД перед тестом, разъединение после."""
#     # Инициализация: старт БД
#     tasks.start_tasks_db(str(tmpdir), 'tiny')
#     # здесь происходит тестирование
#     yield
#     # После тестов: стоп БД
#     tasks.stop_tasks_db()


@pytest.mark.xfail(tasks.__version__ < '0.3.0', reason='not supported until version 0.3.0')
def test_unique_id_1():
    """Вызов unique_id() дважды должен возвращать разные числа."""
    id_1 = tasks.unique_id()
    id_2 = tasks.unique_id()
    assert id_1 != id_2


@pytest.mark.xfail()
def test_unique_id_is_a_duck():
    """Демонстрирование xfail."""
    uid = tasks.unique_id()
    assert uid == 'a duck'


@pytest.mark.xfail()
def test_unique_id_not_a_duck():
    """Демонстрация xpass."""
    uid = tasks.unique_id()
    assert uid != 'a duck'