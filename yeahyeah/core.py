"""Core functionality for yeahyeah launch manager

"""

from pathlib import Path

import click

from yeahyeah.cli_new import root_cli, admin
from yeahyeah.core_new import YeahYeahContext


class YeahYeah:
    """A cli module that has menu items
    """

    def __init__(self):
        self.configuration_path = Path.home() / ".config" / "yeahyeah"
        self.plugins = []
        self.root_cli = root_cli
        self.admin_cli = admin

        self.settings = YeahYeahContext(settings_path=self.configuration_path)

    def add_plugin(self, plugin):
        """Add this plugin to yeahyeah

        This will add all its actions to root_cli directly and all admin actions to root_cli/admin

        Notes
        -----
        Because all actions are added to root_cli directly, actions from different plugins can overwrite each other.
        Yeahyeah does not check this. New actions will overwrite old actions.

        Parameters
        ----------
        plugin: yeahyeah.cli_new.YeahYeahPlugin

        """
        self.plugins.append(plugin)
        for command in plugin.get_commands():
            self.root_cli.add_command(command)

        @click.group(name=plugin.slug, help=f"Admin for {plugin.slug}")
        @click.pass_context
        def plugin_admin(ctx):
            f"""Admin for {plugin.slug}"""
            ctx.obj = self.settings

        for command in plugin.get_admin_commands():
            plugin_admin.add_command(command)
        self.admin_cli.add_command(plugin_admin)


