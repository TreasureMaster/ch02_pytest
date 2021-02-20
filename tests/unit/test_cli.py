from click.testing import CliRunner
from contextlib import contextmanager
import pytest
from tasks.api import Task
import tasks.cli
import tasks.config


@contextmanager
def stub_tasks_db():
    yield


# NEWIT Правильно ли вызывается API?
# mocker - фикстура pytest-mock (это удобный интерфейс для unittest-mock)
def test_list_no_args(mocker):
    # заменяет менеджер контекста заглушкой _tasks_db(), которая ничего не делает
    mocker.patch.object(tasks.cli, '_tasks_db', new=stub_tasks_db)
    # заменяет любые вызовы tasks.list_tasks() из tasks.cli на объект MagicMock (по умолчанию возвращаемым значением пустого списка)
    mocker.patch.object(tasks.cli.tasks, 'list_tasks', return_value=[])
    # 3-я и 4-я строки используют Click CliRunner делают то же, что и вызов списка задач в командной строке
    runner = CliRunner()
    runner.invoke(tasks.cli.tasks_cli, ['list'])
    # использует макет объекта, чтобы убедиться, что вызов API был правильным
    tasks.cli.tasks.list_tasks.assert_called_once_with(None)


# NEWIT Явяляется ли вывод на печать правильным?
# идентичные конструкции, проверяющие вывод
@pytest.fixture()
def no_db(mocker):
    mocker.patch.object(tasks.cli, '_tasks_db', new=stub_tasks_db)

def test_list_print_empty(no_db, mocker):
    mocker.patch.object(tasks.cli.tasks, 'list_tasks', return_value=[])
    runner = CliRunner()
    result = runner.invoke(tasks.cli.tasks_cli, ['list'])
    expected_out = ("  ID      owner  done summary\n"
                    "  --      -----  ---- -------\n")
    assert result.output == expected_out


def test_list_print_many_items(no_db, mocker):
    many_tasks = (
        Task('write chapter', 'Brian', True, 1),
        Task('edit chapter', 'Katie', False, 2),
        Task('modify chapter', 'Brian', False, 3),
        Task('finalize chapter', 'Katie', False, 4),
    )
    mocker.patch.object(tasks.cli.tasks, 'list_tasks', return_value=many_tasks)
    runner = CliRunner()
    result = runner.invoke(tasks.cli.tasks_cli, ['list'])
    expected_output = ("  ID      owner  done summary\n"
                       "  --      -----  ---- -------\n"
                       "   1      Brian  True write chapter\n"
                       "   2      Katie False edit chapter\n"
                       "   3      Brian False modify chapter\n"
                       "   4      Katie False finalize chapter\n")
    assert result.output == expected_output


def test_list_dash_o(no_db, mocker):
    mocker.patch.object(tasks.cli.tasks, 'list_tasks')
    runner = CliRunner()
    runner.invoke(tasks.cli.tasks_cli, ['list', '-o', 'brian'])
    tasks.cli.tasks.list_tasks.assert_called_once_with('brian')

def test_list_dash_dash_owner(no_db, mocker):
    mocker.patch.object(tasks.cli.tasks, 'list_tasks')
    runner = CliRunner()
    runner.invoke(tasks.cli.tasks_cli, ['list', '--owner', 'okken'])
    tasks.cli.tasks.list_tasks.assert_called_once_with('okken')