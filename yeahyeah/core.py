# -*- coding: utf-8 -*-

"""Core functionality for yeahyeah launch manager"""
from pathlib import Path

import click


class YeahYeah:
    """A cli module that has menu items
    """

    def __init__(self):
        self.configuration_path = Path.home() / "yeahyeah_config"
        self.plugins = []
        self.root_cli = self.get_root_cli()
        self.admin_cli = self.admin_cli_group()
        self.root_cli.add_command(self.admin_cli)
        self.admin_cli.add_command(self.install_info_cli_action())

    @staticmethod
    def get_root_cli():
        """Get the base click group for yeahyeah"""

        @click.group()
        def root_cli():
            """Yeahyeah launch things
            """

        return root_cli

    def add_plugin(self, plugin):
        """Add this plugin and all its actions

        Parameters
        ----------
        plugin: YeahYeahPlugin

        """
        self.plugins.append(plugin)
        for pattern in plugin.get_menu_items():
            command = pattern.to_click_command()
            command.help += f" ({plugin.short_slug})"
            self.root_cli.add_command(command)

        @click.group(name=plugin.slug, help=f"Admin for {plugin.slug}")
        def plugin_admin():
            f"""Admin for {plugin.slug}"""
            pass

        for command in plugin.get_admin_commands():
            plugin_admin.add_command(command)
        self.admin_cli.add_command(plugin_admin)

    def admin_cli_group(self):
        """Returns an 'admin' click group containing all admin actions for this plugin"""

        @click.group()
        def admin():
            """Admin options for yeahyeah and plugins"""
            pass

        return admin

    @staticmethod
    def install_info_cli_action():
        """Returns a click action that prints some info on how to get auto-completion to work for yeahyeah
        """
        @click.command()
        def enable_autocompletion():
            """Print information on how to enable command auto-completion"""
            click.echo('Execute the following line in a terminal to enable auto-completion for that terminal only:\n'
                       '\n'
                       '    $ eval "$(_JJ_COMPLETE=source jj)"\n'
                       '\n'
                       'To enable auto completion permanently, run this\n'
                       '\n'
                       '    $ echo "eval $(_JJ_COMPLETE=source jj)" >> ~/.bashrc\n')

        return enable_autocompletion


class YeahYeahMenuItem:
    """Something you can add to the base yeahyeah menu"""

    def __init__(self, name, help_text=None):
        """

        Parameters
        ----------
        name: str
            Name to launch this item with, probably you want to keep this short.
        help_text: str, optional
            Short help message for this item. Defaults to empty string
        """
        self.name = name
        self._help_text = help_text

    @property
    def help_text(self):
        if self.help_text is None:
            return ""
        else:
            return self.help_text

    def to_click_command(self):
        """Return a click command representation of this action

        Returns
        -------
        func
            A function that has been processed by the @click.command() decorator.
            <click_group>.add_command(test) should work

        """
        raise NotImplementedError()


class YeahYeahPlugin:
    """A thing that can generate YeahYeahMenuItems that can be added"""

    def __init__(self, slug, short_slug=None):
        """

        Parameters
        ----------
        slug: str
            short, no space name to use for describing this plugin but also as key for admin functions
        short_slug: str, optional
            Slug which is a short as possible, to append to options help text. For example 'url', or 'path'. Defaults
            to slug
        """
        self.slug = slug
        if not short_slug:
            short_slug = slug
        self.short_slug = short_slug


    def get_menu_items(self):
        """Get all menu items that this plugin has

        Returns
        -------
        List[YeahYeahMenuItem]
            menu items that can be added to a click group using <click_group>.add_command(test)
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
