# -*- coding: utf-8 -*-

"""Console script for yeahyeah.
# usage:

$ pip install - -editable.
$ eval "$(_YEAHYEAH_COMPLETE=source yeahyeah)"
$ eval "$(_JJ_COMPLETE=source jj)"
$ yeahyeah

"""

from yeahyeah.core import YeahYeah
from yeahyeah.url_pattern import UrlPatternsPlugin


jj = YeahYeah()

# add plugins
jj.add_plugin(UrlPatternsPlugin.__from_file_path__(config_file_path=jj.configuration_path / "url_patterns.yaml"))

yeahyeah = jj.root_cli   # base click command line entry point
