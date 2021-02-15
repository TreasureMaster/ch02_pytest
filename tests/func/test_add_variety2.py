"""Тест API tasks.add() функции."""

import pytest
import tasks
from tasks import Task


tasks_to_try = (
    Task('sleep', done=True),
    Task('wake', 'brian'),
    Task('breathe', 'BRIAN', True),
    Task('exercise', 'BrIaN', False)
)

task_ids = ['Task({},{},{})'.format(t.summary, t.owner, t.done) for t in tasks_to_try]


def equivalent(t1, t2):
    """Проверить 2 tasks на эквивалентность."""
    return (
        (t1.summary == t2.summary) and
        (t1.owner == t2.owner) and
        (t1.done == t2.done)
    )

# теперь вместо параметризации теста, происходит параметризация фикстуры
# request - это встроенная фикстура, представляет вызывающее состояние фикстуры.
@pytest.fixture(params=tasks_to_try)
def a_task(request):
    """Без идентификатора."""
    return request.param

def test_add_a(tasks_db, a_task):
    """Использование фикстуры a_task (без ids)."""
    task_id = tasks.add(a_task)
    t_from_db = tasks.get(task_id)
    assert equivalent(t_from_db, a_task)


@pytest.fixture(params=tasks_to_try, ids=task_ids)
def b_task(request):
    """Использование списка идентификаторов."""
    return request.param

def test_add_b(tasks_db, b_task):
    """использование фикстуры b_task с идентификаторами."""
    task_id = tasks.add(b_task)
    t_from_db = tasks.get(task_id)
    assert equivalent(t_from_db, b_task)

# Генерация идентификаторов с помощью функции
def id_func(fixture_value):
    """Функция для генерации идентификаторов."""
    t = fixture_value
    return 'Task({},{},{})'.format(t.summary, t.owner, t.done)

@pytest.fixture(params=tasks_to_try, ids=id_func)
def c_task(request):
    """Использование функции (id_func) для генерации идентификаторов."""
    return request.param

def test_add_c(tasks_db, c_task):
    """Использование фикстуры с генерированными идентификаторами."""
    task_id = tasks.add(c_task)
    t_from_db = tasks.get(task_id)
    assert equivalent(t_from_db, c_task)