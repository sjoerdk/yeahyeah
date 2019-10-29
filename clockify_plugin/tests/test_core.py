import pytest

from clockify_plugin.cli import main
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
def mock_clockify_runner(a_clockify_context):
    """Runner that injects a clockify context. Used for all subcommands"""
    return MockContextCliRunner(mock_context=a_yeahyeah_context)


def test_main(mock_yeahyeah_runner):
    """Basic test. Just should not raise exceptions"""
    result = mock_yeahyeah_runner.invoke(main, catch_exceptions=False)
    assert result.exit_code == 0


def test_main_object_conversion(mock_yeahyeah_runner):
    """Is YeahYeahContext translated into ClockifyPluginContext correctly?"""
    result = mock_yeahyeah_runner.invoke(main, ['status'], catch_exceptions=False)
    assert result.exit_code == 0




