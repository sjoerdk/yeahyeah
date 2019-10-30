"""Main yeahyeah command line interface methods.

These are all the methods that are available even without any plugins
"""
from pathlib import Path

import click


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


class YeahYeahContext:
    """Core yeahyeah context object. This gets passed to all plugins by default when calling any plugin method

    """
    def __init__(self, settings_path):
        """

        Parameters
        ----------
        settings_path: Pathlike
            Path to the folder where any settings can be stored
        """
        self.settings_path = settings_path


def get_settings():
    """Core yeahyeah settings that get passed to each plugin"""
    return YeahYeahContext(settings_path=Path.home() / ".config" / "yeahyeah")
