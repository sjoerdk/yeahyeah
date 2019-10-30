from unittest import mock
from unittest.mock import Mock

import click
import pytest
from click.testing import CliRunner
from clockifyclient.client import APISession
from clockifyclient.exceptions import ClockifyClientException
from clockifyclient.models import Project

from clockify_plugin.cli import main, stop, projects, add, find_project
from clockify_plugin.context import ClockifyPluginContext
from tests.conftest import MockContextCliRunner
from yeahyeah.core_new import YeahYeahContext


@pytest.fixture
def a_yeahyeah_context(tmpdir):
    """Context as passed from yeahyeah main application. Mocked to have temp settings_dir"""
    return YeahYeahContext(settings_path=tmpdir)


@pytest.fixture
def a_clockify_context():
    """Context as passed from clockifyplugin.main()"""
    return ClockifyPluginContext(api_key='testapikey', api_url='testurl.localhost')


@pytest.fixture
def mock_yeahyeah_runner(a_yeahyeah_context):
    """Runner that injects a yeahyeah context. Only used for main()"""
    return MockContextCliRunner(mock_context=a_yeahyeah_context)


@pytest.fixture
def mock_api_session():
    return Mock(spec=APISession)


@pytest.fixture
def mock_clockify_runner(mock_api_session):
    """Runner that injects a clockify context that mocks actual calls to clockify API. Used for all subcommands"""
    context = ClockifyPluginContext(api_key='mockkey', api_url='mockurl')
    context.session = mock_api_session
    return MockContextCliRunner(mock_context=context)


@pytest.fixture
def some_projects():
    return [Project(obj_id=None, name='project1'),
            Project(obj_id=None, name='project2'),
            Project(obj_id=None, name='PRo-ject3')]


def test_main(mock_yeahyeah_runner):
    """Basic test. Just should not raise exceptions"""
    result = mock_yeahyeah_runner.invoke(main, catch_exceptions=False)
    assert result.exit_code == 0


def test_main_object_conversion(mock_yeahyeah_runner):
    """Is YeahYeahContext translated into ClockifyPluginContext correctly?"""
    result = mock_yeahyeah_runner.invoke(main, ['status'], catch_exceptions=False)
    assert result.exit_code == 0


def test_stop(mock_api_session, mock_clockify_runner):
    result = mock_clockify_runner.invoke(stop, catch_exceptions=False)
    assert result.exit_code == 0
    assert mock_api_session.stop_timer.called


@pytest.mark.parametrize('cli_function, params', [(stop, None),
                                                  (add, ['a message']),
                                                  (projects, None)])
def test_clockify_exceptions(mock_api_session, mock_clockify_runner, cli_function, params):
    """Clockify API Exceptions should be caught and displayed, instead of raised"""
    for func in [mock_api_session.stop_timer,
                 mock_api_session.get_projects,
                 mock_api_session.get_default_workspace,
                 mock_api_session.get_user,
                 mock_api_session.add_time_entry_object,
                 mock_api_session.add_time_entry]:
        func.side_effect = ClockifyClientException('Clockify API is completely broken')

    result = mock_clockify_runner.invoke(cli_function, args=params, catch_exceptions=False)
    assert result.exit_code == 1
    assert "completely broken" in result.output


def test_find_projects(some_projects):
    assert find_project(some_projects, 'proj') == some_projects[0]
    assert find_project(some_projects, 'project2') == some_projects[1]
    assert find_project(some_projects, 'pro-') == some_projects[2]

    with pytest.raises(click.BadParameter) as e:
        find_project(some_projects, 'unknown')
    assert "Could not find project" in str(e.value)


def test_projects(mock_api_session, mock_clockify_runner):
    mock_api_session.get_projects.return_value = [Mock(), Mock()]
    result = mock_clockify_runner.invoke(projects, catch_exceptions=False)
    assert result.exit_code == 0
    assert mock_api_session.get_projects.called

    mock_api_session.get_projects.return_value = []
    assert 'No projects' in mock_clockify_runner.invoke(projects).output


@pytest.mark.parametrize('args', ['some message',
                                  'some message -p project1',
                                  '-p pro- some different message',
                                  'some message -t -10',
                                  'some message -t 15:10'])
def test_add_succes(mock_api_session, mock_clockify_runner, some_projects, args):
    """Add commands that should work"""
    mock_api_session.get_projects.return_value = some_projects

    result = mock_clockify_runner.invoke(add, args=args, catch_exceptions=False)
    assert result.exit_code == 0
    assert mock_api_session.add_time_entry.called


@pytest.mark.parametrize('args', ['',
                                  'some message -p unknown_project',
                                  '-s what is -s',
                                  'some message -t 1536:3434',
                                  'some message -t '])
def test_add_fail(mock_api_session, mock_clockify_runner, some_projects, args):
    """Add commands that should not work but not raise exceptions either"""
    mock_api_session.get_projects.return_value = some_projects

    result = mock_clockify_runner.invoke(add, args=args, catch_exceptions=False)
    assert result.exit_code != 0
    assert not mock_api_session.add_time_entry.called


@pytest.mark.parametrize('args, expected_message', [('some message', "some message"),
                                                    ('no_space_message', "no_space_message"),
                                                    ('some message -p project1', "some message"),
                                                    ('-p pro- some different message', "some different message"),
                                                    ('-p proj some message -t -10', "some message"),
                                                    ('some message -t 15:10', "some message")])
def test_add_message_parsing(mock_api_session, mock_clockify_runner, some_projects, args, expected_message):
    """Is message parsed properly, even with confusing flags around it?"""
    mock_api_session.get_projects.return_value = some_projects
    result = mock_clockify_runner.invoke(add, args=args, catch_exceptions=False)
    assert result.exit_code == 0
    assert mock_api_session.add_time_entry.call_args[1]['description'] == expected_message
