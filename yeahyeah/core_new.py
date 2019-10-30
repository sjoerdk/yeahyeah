"""Migrating to a better way of using click.
Old way:  Generate all click functions inside classes and kind of hack in the 'self' object by attaching the class self
to the generated functions, like this:

class plugin:

    def get_click_command(self):

        @click.command()
        def a_command():
            self.do_thing()  # self is kind of strangely inserted here

        return a_command


The new way is to use proper click command interleaving with pass_context() and passing around settings objects:

@click.command()
@click.pass_context
def a_command(ctx):
    ctx.do_thing()


This makes the code less convoluted, more testable and more separated.


However I can't do all this refactoring in one go. Time constraints. So doing this step by step. Anything in the new
scheme gets moved here to core_new.py When refactoring is complete this gets renamed to core.py
"""
from pathlib import Path

import click

from yeahyeah.cli_new import root_cli, admin, YeahYeahContext


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
        plugin: yeahyeah.core_new.YeahYeahPlugin

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


class YeahYeahPlugin:
    """Some named thing that adds launchable commands to yeahyeah"""

    slug = 'BasePlugin'  # Short, no space name to use for describing this plugin but also as key for admin functions
    short_slug = 'Base'   # Shorter slug, to append to options help text. For example 'url', or 'path'

    def __init__(self, context: YeahYeahContext):
        """

        Parameters
        ----------
        context: YeahYeahContext
            Context of the root yeahyeah module
        """
        raise NotImplemented()

    def get_commands(self):
        """All Commands for this plugin

        Returns
        -------
        List[click.Command]
            All click commands that can be executed as part of this plugin
        """
        raise NotImplementedError()

    def get_admin_commands(self):
        """Action to do admin tasks for this plugin, if any

        Returns
        -------
        List[click.Command]
            List of click commands that can be used to admin this plugin

        """
        raise NotImplementedError()
