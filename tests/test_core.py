#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pathlib import Path

import pytest
from click.testing import CliRunner

from yeahyeah_plugins.clockify_plugin.core import ClockifyPlugin
from yeahyeah_plugins.path_item_plugin.core import PathItemPlugin
from yeahyeah_plugins.url_pattern_plugin.core import UrlPatternsPlugin
from tests.conftest import MockContextCliRunner

from yeahyeah.core import YeahYeah


@pytest.fixture()
def a_yeahyeah_instance(tmpdir):
    """YeahYeah instance with tmp configuration path and default yeahyeah_plugins """

    jj = YeahYeah(configuration_path=Path(str(tmpdir)))

    jj.add_plugin(ClockifyPlugin(context=jj.context))
    jj.add_plugin(PathItemPlugin.init_from_context(context=jj.context))
    jj.add_plugin(UrlPatternsPlugin.init_from_context(context=jj.context))

    return jj


@pytest.fixture()
def mock_cli_runner(a_yeahyeah_instance):
    """Runner that injects default context into each call, configuration path is tmpdir"""
    return MockContextCliRunner(mock_context=a_yeahyeah_instance.context)


def test_command_line_interface(a_yeahyeah_instance, mock_cli_runner):
    """Test the CLI."""
    result = mock_cli_runner.invoke(a_yeahyeah_instance.root_cli)
    assert result.exit_code == 0


def test_command_admin_status(a_yeahyeah_instance, mock_cli_runner):
    """Test the yeahyeah admin command"""
    result = mock_cli_runner.invoke(a_yeahyeah_instance.root_cli, args='admin yeahyeah status'.split(' '))
    assert result.exit_code == 0
