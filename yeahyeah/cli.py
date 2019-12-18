# -*- coding: utf-8 -*-

"""Console script for yeahyeah.
# usage:

$ pip install - -editable.
$ eval "$(_YEAHYEAH_COMPLETE=source yeahyeah)"
$ eval "$(_JJ_COMPLETE=source jj)"
$ yeahyeah

"""
from pathlib import Path

from yeahyeah.core import YeahYeah

configuration_path = Path.home() / ".config" / "yeahyeah"

jj = YeahYeah(configuration_path=configuration_path)

plugin_classes = ['yeahyeah_plugins.clockify_plugin.core.ClockifyPlugin',
                  'yeahyeah_plugins.ad_plugin.core.ADPlugin',
                  'yeahyeah_plugins.path_item_plugin.core.PathItemPlugin',
                  'yeahyeah_plugins.url_pattern_plugin.core.UrlPatternsPlugin']

for class_ref in plugin_classes:
    jj.add_plugin(class_ref)

yeahyeah = jj.root_cli  # base click command line entry point