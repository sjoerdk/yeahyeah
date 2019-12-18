from unittest.mock import Mock

import click
import pytest

from yeahyeah.plugin_testing import MockContextCliRunner
from yeahyeah.context import YeahYeahContext
from yeahyeah_plugins.ad_plugin.cli import main, find_z_number, translate
from yeahyeah_plugins.ad_plugin.context import ADPluginContext
from umcnad.core import ADConnection


@pytest.fixture
def a_yeahyeah_context(tmpdir):
    """Context as passed from yeahyeah main application. Mocked to have temp
    settings_dir"""
    return YeahYeahContext(settings_path=tmpdir)


@pytest.fixture
def an_ad_context():
    """Context as passed from clockifyplugin.main()"""
    return ADPluginContext(server_url="localhost", bind_dn="test_bind_dn")


@pytest.fixture
def an_ad_context_with_search(an_ad_context, person_list):
    an_ad_context.search_people = Mock(return_value=person_list)


@pytest.fixture
def mock_yeahyeah_runner(a_yeahyeah_context):
    """Runner that injects a yeahyeah context. Only used for main()"""
    return MockContextCliRunner(mock_context=a_yeahyeah_context)


@pytest.fixture
def mock_adcontext_runner(an_ad_context):
    """Runner that injects a ADPluginContext. This context should be passed to most
    adplugin functions"""
    return MockContextCliRunner(mock_context=an_ad_context)


@pytest.fixture()
def mock_ad_connection(monkeypatch):
    """A mock connection object to AD. Makes sure no actual AD is called"""
    mock_connection = Mock(spec=ADConnection)
    monkeypatch.setattr(
        "yeahyeah_plugins.ad_plugin.context.ADConnection", mock_connection
    )
    return mock_connection


def test_main(mock_yeahyeah_runner):
    """Basic test. Just should not raise exceptions"""
    result = mock_yeahyeah_runner.invoke(main, catch_exceptions=False)
    assert result.exit_code == 0


def test_main_status(mock_yeahyeah_runner, mock_ad_connection):
    """Is YeahYeahContext translated into ClockifyPluginContext correctly?"""
    result = mock_yeahyeah_runner.invoke(main, ["status"], catch_exceptions=False)
    assert result.exit_code == 0


def test_find_z_number(mock_adcontext_runner, an_ad_context_with_search, person_list):
    """Are the people found displayed properly?"""
    result = mock_adcontext_runner.invoke(
        find_z_number, args="z123345 Z123456", catch_exceptions=False
    )
    assert result.exit_code == 0


def test_translate(mock_adcontext_runner, an_ad_context_with_search, person_list):
    """Test translating running text"""
    result = mock_adcontext_runner.invoke(
        translate, args="user z123456 was bad", catch_exceptions=False
    )
    assert result.exit_code == 0
    assert result.output == "user Testo, Jane (z123456) was bad\n"

    assert (
        mock_adcontext_runner.invoke(translate, args="user z123123 was bad").output
        == "user z123123 was bad\n"
    )


def test_translate_empty(mock_adcontext_runner, an_ad_context_with_search, person_list):
    """should not be a problem"""
    result = mock_adcontext_runner.invoke(
        translate, catch_exceptions=False
    )
    assert result.exit_code == 0
    assert result.output == ""
