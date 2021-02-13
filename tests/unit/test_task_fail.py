"""используем Task type для отображения сбоев тестов."""

from tasks import Task


def test_task_equality():
    """Разные задачи не должны быть равными."""
    t1 = Task('sit there', 'brian')
    t2 = Task('do something', 'okken')
    assert t1 == t2


def test_dict_equality():
    """Различные задачи, сравниваемые как dicts, не должны быть равны."""
    t1_dict = Task('make sandwich', 'okken')._asdict()
    t2_dict = Task('make sandwich', 'okkem')._asdict()
    assert t1_dict == t2_dict