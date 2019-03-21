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




