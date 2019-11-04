from yeahyeah_plugins.clockify_plugin.cli import main, edit_settings
from yeahyeah.core import YeahYeahPlugin
from yeahyeah.context import YeahYeahContext


class ClockifyPlugin(YeahYeahPlugin):

    slug = "clockify"
    short_slug = "clock"

    def __init__(self, context: YeahYeahContext):
        """Plugin that controls clockify

        Parameters
        ----------
        context: yeahyeah.context.YeahYeahContext
            Context of the root yeahyeah module
        """
        pass

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
