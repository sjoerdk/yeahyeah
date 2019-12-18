import importlib
from unittest.mock import Mock

from click.testing import CliRunner


def test_cli(monkeypatch):
    mock = Mock()
    monkeypatch.setattr('yeahyeah.cli.YeahYeah', mock)
    importlib.import_module('yeahyeah.cli')