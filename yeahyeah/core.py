
import click


class YeahYeahContext:
    """Core yeahyeah context object. This gets passed to all plugins on init() and to any method call

    """
    def __init__(self, settings_path):
        """

        Parameters
        ----------
        settings_path: Pathlike
            Path to the folder where any context can be stored
        """
        self.settings_path = settings_path


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

        admin_group.add_command(self.enable_autocompletion)
        return admin_group

    @staticmethod
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
