# -*- coding: utf-8 -*-

"""Console script for yeahyeah.
# usage:

$ pip install - -editable.
$ eval "$(_YEAHYEAH_COMPLETE=source yeahyeah)"
$ eval "$(_JJ_COMPLETE=source jj)"
$ yeahyeah

"""
from pathlib import Path

from plugins.clockify_plugin.core import ClockifyPlugin
from yeahyeah.core import YeahYeah
from plugins.path_item_plugin.core import PathItemPlugin
from plugins.url_pattern_plugin.core import UrlPatternsPlugin

jj = YeahYeah(configuration_path=Path.home() / ".config" / "yeahyeah")

jj.add_plugin(ClockifyPlugin(context=jj.context))
jj.add_plugin(PathItemPlugin.init_from_context(context=jj.context))
jj.add_plugin(UrlPatternsPlugin.init_from_context(context=jj.context))

yeahyeah = jj.root_cli   # base click command line entry point
