#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `yeahyeah` package."""
import webbrowser
from unittest.mock import Mock

import pytest

from click.testing import CliRunner

from yeahyeah import cli
from yeahyeah.core import YeahYeah
from yeahyeah.url_pattern import UrlPatternsPlugin



@pytest.fixture()
def mock_web_browser(monkeypatch):
    """Mock the python standard webbrowser
    """
    mock_web_browser = Mock(spec=webbrowser)
    monkeypatch.setattr("yeahyeah.url_pattern.webbrowser", mock_web_browser)
    return mock_web_browser


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.yeahyeah)
    assert result.exit_code == 0


def test_ticket(mock_web_browser, yeahyeah_instance):
    """Test online searching with variable replacement"""
    runner = CliRunner()
    result = runner.invoke(yeahyeah_instance.root_cli, ["test5", "some_query"])
    assert result.exit_code == 0
    assert result.output == "loading https://searchsome_query\n"

    result = runner.invoke(cli.yeahyeah, ["wiki"])
    assert 'Missing argument "ARTICLE_SLUG"' in result.output


def test_plugin(url_pattern_list, mock_web_browser):
    yeahyeah = YeahYeah()
    plugin = UrlPatternsPlugin(pattern_list=url_pattern_list)
    yeahyeah.add_plugin(plugin)

    # after adding plugin you should be able to call one of the methods
    runner = CliRunner()
    assert (
        runner.invoke(yeahyeah.root_cli, ["test1", "val1", "val2"]).output
        == "loading https://hostval1/somethingval2.php\n"
    )
