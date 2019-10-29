import click

from clockify_plugin.cli import main, edit_settings
from clockify_plugin.context import default_settings_file_name, default_context
from yeahyeah.cli_new import YeahYeahPlugin
from yeahyeah.core_new import YeahYeahContext
from yeahyeah.persistence import JSONSettingsFile


class ClockifyPlugin(YeahYeahPlugin):

    slug = "clockify"
    short_slug = "clock"

    def __init__(self, context: YeahYeahContext):
        """Plugin that controls clockify

        Parameters
        ----------
        context: YeahYeahContext
            Context of the root yeahyeah module
        """
        settings_file = JSONSettingsFile(path=context.settings_path / default_settings_file_name)
        if not settings_file.exists():
            click.echo(f"Settings file not found. Writing default settings to {settings_file.path}")
            settings_file.save(dict_in=default_context.to_dict())
        self.settings = settings_file.load()

    def get_commands(self):
        """

        Returns
        -------
        List[click.Command]
        """

        return [main]

    def get_admin_commands(self):
        """

        Returns
        -------
        List[click.Command]
            list of click commands that can be used to admin this plugin

        """

        return [edit_settings]

