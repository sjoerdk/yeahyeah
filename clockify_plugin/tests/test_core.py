from unittest.mock import Mock

import pytest
from clockifyclient.client import APISession
from clockifyclient.exceptions import ClockifyClientException

from clockify_plugin.cli import main, stop
from clockify_plugin.context import ClockifyPluginContext
from tests.conftest import MockContextCliRunner
from yeahyeah.core_new import YeahYeahContext


@pytest.fixture
def a_yeahyeah_context(tmpdir):
    """Context as passed from yeahyeah main application"""
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


def test_stop_exception(mock_api_session, mock_clockify_runner):
    mock_api_session.stop_timer.side_effect = ClockifyClientException('Clockify API is completely broken')
    result = mock_clockify_runner.invoke(stop, catch_exceptions=False)
    assert result.exit_code == 1
    assert mock_api_session.stop_timer.called
    assert "completely broken" in result.output
    assert "stopped" not in result.output
