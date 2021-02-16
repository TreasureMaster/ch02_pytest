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

@pytest.mark.xfail()
def test_unique_id_1():
    """Вызов unique_id() дважды должен возвращать разные числа."""
    id_1 = tasks.unique_id()
    id_2 = tasks.unique_id()
    assert id_1 != id_2