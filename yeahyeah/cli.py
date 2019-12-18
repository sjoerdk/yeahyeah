# -*- coding: utf-8 -*-

"""Console script for yeahyeah
# usage:

$ pip install --editable .
$ eval "$(_YEAHYEAH_COMPLETE=source yeahyeah)"
$ eval "$(_JJ_COMPLETE=source jj)"
$ yeahyeah

"""
from pathlib import Path

import click

from yeahyeah.config import CORE_CONFIG_PATH
from yeahyeah.core import YeahYeah
from yeahyeah.persistence import YeahYeahPersistenceException

jj = YeahYeah(configuration_path=CORE_CONFIG_PATH)

# get plugins

#plugin_classes = ['yeahyeah_plugins.clockify_plugin.core.ClockifyPlugin',
#                  'yeahyeah_plugins.ad_plugin.core.ADPlugin',
#                  'yeahyeah_plugins.path_item_plugin.core.PathItemPlugin',
#                  'yeahyeah_plugins.url_pattern_plugin.core.UrlPatternsPlugin']

try:
    plugin_classes = jj.get_settings().plugin_paths
except YeahYeahPersistenceException as e:
    click.echo(f'Could not read settings file. Please'
               f' check {jj.settings_file_path}. Original error: {e}')
else:
    for class_ref in plugin_classes:
        jj.add_plugin(class_ref)

yeahyeah = jj.root_cli  # base click command line entry point