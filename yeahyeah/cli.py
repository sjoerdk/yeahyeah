# -*- coding: utf-8 -*-

"""Console script for yeahyeah.
# usage:

$ pip install - -editable.
$ eval "$(_YEAHYEAH_COMPLETE=source yeahyeah)"
$ eval "$(_JJ_COMPLETE=source jj)"
$ yeahyeah

"""
from clockify_plugin.core import ClockifyPlugin
from yeahyeah.plugins_old.path_items import PathItemPlugin
from yeahyeah.plugins_old.url_patterns import UrlPatternsPlugin
from yeahyeah.core import YeahYeah


jj = YeahYeah()

# add plugins_old
jj.add_plugin(UrlPatternsPlugin.__from_file_path__(config_file_path=jj.configuration_path / "url_patterns.yaml"))
jj.add_plugin(PathItemPlugin.__from_file_path__(config_file_path=jj.configuration_path / "path_items.yaml"))
jj.add_plugin(ClockifyPlugin.__from_file_path__(config_file_path=jj.configuration_path / "clockify.json"))

yeahyeah = jj.root_cli   # base click command line entry point
