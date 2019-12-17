from yeahyeah_plugins.ad_plugin.cli import main, edit_settings
from yeahyeah.core import YeahYeahPlugin
from yeahyeah.context import YeahYeahContext


class ADPlugin(YeahYeahPlugin):

    slug = "umcn_AD"
    short_slug = "umcnAD"

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
