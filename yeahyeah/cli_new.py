"""Main yeahyeah command line interface methods.

These are all the methods that are available even without any plugins
"""
from pathlib import Path

import click

from yeahyeah.core_new import YeahYeahContext


def get_settings():
    """Core yeahyeah settings that get passed to each plugin"""
    return YeahYeahContext(settings_path=Path.home() / ".config" / "yeahyeah")


@click.group()
@click.pass_context
def root_cli(ctx):
    """Yeahyeah launch things
    """

    ctx.obj = get_settings()
    return root_cli


@click.group()
def admin():
    """Admin options for yeahyeah and plugins_old"""
    pass


@click.command()
def enable_autocompletion():
    """Print information on how to enable command auto-completion"""
    click.echo('Execute the following line in a terminal to enable auto-completion for that terminal only:\n'
               '\n'
               '    $ eval "$(_JJ_COMPLETE=source jj)"\n'
               '\n'
               'To enable auto completion permanently, run this\n'
               '\n'
               "    $ echo 'eval \"$(_JJ_COMPLETE=source jj)\"' >> ~/.bashrc\n")


admin.add_command(enable_autocompletion)
root_cli.add_command(admin)


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
