
import click

from yeahyeah.context import YeahYeahContext
from yeahyeah.decorators import pass_yeahyeah_context


class YeahYeah:
    """A cli module that has menu items
    """

    def __init__(self, configuration_path):
        """

        Parameters
        ----------
        configuration_path: Pathlike
            Path to a location where plugins can read and write settings
        """
        self.configuration_path = configuration_path
        self.plugins = []

        self.root_cli = self.get_root_cli()
        self.admin_cli = self.get_admin_group()
        self.root_cli.add_command(self.admin_cli)

        self.context = YeahYeahContext(settings_path=self.configuration_path)

    def add_plugin(self, plugin):
        """Add this plugin to yeahyeah

        This will add all its actions to root_cli directly and all admin actions to root_cli/admin

        Notes
        -----
        Because all actions are added to root_cli directly, actions from different plugins can overwrite each other.
        Yeahyeah does not check this. New actions will overwrite old actions.

        Parameters
        ----------
        plugin: yeahyeah.core.YeahYeahPlugin

        """
        self.plugins.append(plugin)
        for command in plugin.get_commands():
            self.root_cli.add_command(command)

        @click.group(name=plugin.slug, help=f"Admin for {plugin.slug}")
        @click.pass_context
        def plugin_admin(ctx):
            f"""Admin for {plugin.slug}"""
            ctx.obj = self.context

        for command in plugin.get_admin_commands():
            plugin_admin.add_command(command)
        self.admin_cli.add_command(plugin_admin)

    def get_root_cli(self):
        """Create yeahyeah root group

        Notes
        -----
        Notice injection of self. Together with status() This is the only method allowed to do so. All other methods
        have to make do with just a YeahYeahContext object
        """
        @click.group()
        @click.pass_context
        def root_cli(ctx):
            """Yeahyeah launch things
            """

            ctx.obj = self.context
            return root_cli
        return root_cli

    def get_admin_group(self):
        @click.group(name='admin')
        def admin_group():
            """Admin options for yeahyeah and plugins"""
            pass

        @click.group(name='yeahyeah')
        def yeahyeah_group():
            """Admin options for yeahyeah itself"""
            pass

        admin_group.add_command(yeahyeah_group)
        yeahyeah_group.add_command(self.enable_autocompletion)
        yeahyeah_group.add_command(self.get_status_command())

        return admin_group

    def get_status_command(self):
        """Create the command to show this yeahyeah instance's status.

        Notes
        -----
        like main(), status command also gets this slightly smelly access to self. This makes it possible
        for the command to inspect all installed plugins etc.
        """

        @click.command()
        @pass_yeahyeah_context
        def status(ctx: YeahYeahContext):
            """Configuration and status"""
            click.echo("YeahYeah launch status:")
            click.echo(f"settings folder: '{self.configuration_path}'")
            click.echo(f"{len(self.plugins)} plugins activated: [{', '.join([x.slug for x in self.plugins])}]")
            click.echo(f"{len(self.root_cli.commands)} commands in main menu")

        return status

    @staticmethod
    @click.command()
    def enable_autocompletion():
        """Instructions to enable auto-completion"""
        click.echo('Execute the following line in a terminal to enable auto-completion for that terminal only:\n'
                   '\n'
                   '    $ eval "$(_JJ_COMPLETE=source jj)"\n'
                   '\n'
                   'To enable auto completion permanently, run this\n'
                   '\n'
                   "    $ echo 'eval \"$(_JJ_COMPLETE=source jj)\"' >> ~/.bashrc\n")


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

    def __str__(self):
        return f"YeahYeah plugin '{self.slug}'"

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
