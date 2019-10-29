# -*- coding: utf-8 -*-

"""Console script for yeahyeah.
# usage:

$ pip install - -editable.
$ eval "$(_YEAHYEAH_COMPLETE=source yeahyeah)"
$ eval "$(_JJ_COMPLETE=source jj)"
$ yeahyeah

"""
from clockify_plugin.core import ClockifyPlugin
from yeahyeah.core_new import YeahYeahContext
from yeahyeah.plugins_old.path_items import PathItemPlugin
from yeahyeah.plugins_old.url_patterns import UrlPatternsPlugin
from yeahyeah.core import YeahYeah


jj = YeahYeah()
context = YeahYeahContext(settings_path=jj.configuration_path)

jj.add_plugin(ClockifyPlugin(context=context))
jj.add_plugin(PathItemPlugin.init_from_context(context=context))
jj.add_plugin(UrlPatternsPlugin.init_from_context(context=context))

yeahyeah = jj.root_cli   # base click command line entry point
