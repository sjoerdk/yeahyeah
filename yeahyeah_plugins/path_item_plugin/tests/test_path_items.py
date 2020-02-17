#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pathlib import Path
from unittest.mock import Mock

import pytest
from click.testing import CliRunner

from yeahyeah_plugins.path_item_plugin.core import PathItemPlugin
from yeahyeah.core import YeahYeah


@pytest.fixture(autouse=True)
def disable_click_echo(monkeypatch):
    """Don't print click.echo to console. Click runner disables this, but not
    all tests use click runner to invoke all commands. So this is needed"""
    monkeypatch.setattr("yeahyeah.core.click.echo", Mock())


def test_path_item_plugin(path_item_list, tmpdir):

    yeahyeah = YeahYeah(configuration_path=tmpdir)
    plugin = PathItemPlugin(item_list=path_item_list)
    yeahyeah.add_plugin_instance(plugin)

    assert len(plugin.get_commands()) == 2


def test_path_item_plugin_no_file(path_item_list, tmpdir):
    plugin = PathItemPlugin(item_list=path_item_list)
    plugin.assert_config_file(Path(tmpdir) / "path_item_config_test.txt")


def test_url_pattern_plugin_admin_add__remove_list_record(yeahyeah_instance):
    runner = CliRunner()
    path_item_plugin = yeahyeah_instance.plugins[1]

    assert len(path_item_plugin.item_list) == 2

    response = runner.invoke(
        yeahyeah_instance.admin_cli,
        "path_items add a_path /test/something/folder"
    )
    assert response.exit_code == 0
    assert len(path_item_plugin.item_list) == 3

    response = runner.invoke(yeahyeah_instance.admin_cli, "path_items list")

    assert response.exit_code == 0

    response = runner.invoke(
        yeahyeah_instance.admin_cli,
        "path_items remove a_path".split(" ")
    )
    assert response.exit_code == 0
    assert len(path_item_plugin.item_list) == 2

