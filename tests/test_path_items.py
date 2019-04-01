#!/usr/bin/env python
# -*- coding: utf-8 -*-

from click.testing import CliRunner

from plugins.path_items import PathItemPlugin
from tests import RESOURCE_PATH
from yeahyeah.core import YeahYeah


def test_path_item_plugin(path_item_list):

    yeahyeah = YeahYeah()
    plugin = PathItemPlugin(item_list=path_item_list)
    yeahyeah.add_plugin(plugin)

    assert len(plugin.get_menu_items()) == 2


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

