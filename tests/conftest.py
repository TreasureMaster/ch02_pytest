"""Для совместного использования фикстур разными тестами используется файл conftest.py."""

import pytest
import tasks
from tasks import Task, UninitializedDatabase


# tmpdir является областью действия функции, tmpdir_factory - сеанса
# Меняем область действия, т.к. нет смысла создавать БД для каждого теста в отдельности.
@pytest.fixture(scope='session', params=['tiny', 'mongo'])
def tasks_db_session(tmpdir_factory, request):
    """Соединение с БД перед тестом, разъединение после."""
    temp_dir = tmpdir_factory.mktemp('temp')
    tasks.start_tasks_db(str(temp_dir), request.param)
    yield
    tasks.stop_tasks_db()

# tmpdir также является встроенной фикстурой pytest
@pytest.fixture()
def tasks_db(tasks_db_session):
    """Пустая БД tasks."""
    tasks.delete_all()
    # """Подключение к БД перед тестами, отключение после."""
    # # Инициализация: старт БД
    # tasks.start_tasks_db(str(tmpdir), 'tiny')

    # # здесь происходит тестирование
    # yield

    # # Завершение работы: стоп БД
    # tasks.stop_tasks_db()

# Памятка об интерфейсе конструктора Task
# Task(summary=None, owner=None, done=False, id=None)
# summary - то, что требуется (задание)
# owner и done являются необязательными
# id задается базой данных

# Фикстуры данных также работают один раз за сессию
@pytest.fixture(scope='session')
def tasks_just_a_few():
    """Все резюме и владельцы уникальны."""
    return (
        Task('Write some code', 'Brian', True),
        Task("Code review Brian's code", 'Katie', False),
        Task('Fix what Brian did', 'Michelle', False)
    )


@pytest.fixture(scope='session')
def tasks_mult_per_owner():
    """Несколько владельцев с несколькими задачами каждый."""
    return (
        Task('Make a cookie', 'Raphael'),
        Task('Use an emoji', 'Raphael'),
        Task('Move to Berlin', 'Raphael'),

        Task('Create', 'Michelle'),
        Task('Inspire', 'Michelle'),
        Task('Encourage', 'Michelle'),

        Task('Do a handstand', 'Daniel'),
        Task('Write some books', 'Daniel'),
        Task('Eat ice cream', 'Daniel')
    )


# использование фикстур для построения других фикстур
@pytest.fixture()
def db_with_3_tasks(tasks_db, tasks_just_a_few):
    """Подключение БД с 3 задачами, все уникальны."""
    for t in tasks_just_a_few:
        tasks.add(t)

@pytest.fixture()
def db_with_multi_per_owner(tasks_db, tasks_mult_per_owner):
    """Подключение БД с 9 задачами, 3 пользователями по 3 задачи у каждого."""
    for t in tasks_mult_per_owner:
        tasks.add(t)


# Хук pytest, добавляющий команду, разрешающую нижеследующие хуки
def pytest_addoption(parser):
    """Включает nice функцию с опцией --nice."""
    group = parser.getgroup('nice')
    group.addoption('--nice', action='store_true', help='nice: turn failures into opportunities')

# WARNING глобальная pytest.config удалена в pytest 5.0.0 (пока не будем исследовать замену из-за нехватки времени)
# Хук pytest для изменения заголовка теста
def pytest_report_header():
    """Благодарность тестеру за выполнение тестов."""
    if pytest.config.getoption('nice'):
        return "Thanks for running the tests."

# Хук pytest для изменения вывода информации о тесте с F на О, например
def pytest_report_teststatus(report):
    """Превращает неудачи в возможности."""
    if report.when == 'call':
        if report.failed and pytest.config.getoption('nice'):
            return (report.outcome, 'O', 'OPPORTUNITY for improvement')