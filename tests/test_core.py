#!/usr/bin/env python
# -*- coding: utf-8 -*-

from click.testing import CliRunner

from yeahyeah import cli
from yeahyeah.core import YeahYeah
from yeahyeah.plugins_old.url_patterns import UrlPatternsPlugin


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.yeahyeah)
    assert result.exit_code == 0
