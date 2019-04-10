import platform
import subprocess

import click

from yeahyeah.core import YeahYeahPlugin, SerialisableMenuItem, MenuItemList


class WindowItem(SerialisableMenuItem):
    """A description of a window in a GUI

    For performing automated tasks on gui windows, like activating.
    """

    def __init__(self, name, pattern, help_text=None):
        """

        Parameters
        ----------
        name: str
            name of this menuitem. Is also key
        pattern: str
            string to match when trying to do things to this window
        help_text: str, optional
            Help text to show in menu. Defaults to 'Raise <name>'

        """
        super().__init__(name, help_text)

        self.pattern = pattern

    def __str__(self):
        return f"Window {self.name}:{self.pattern}"

    def get_parameters(self):
        return {'pattern': self.pattern}

    def to_click_command(self):
        """Return a click command that raises this window if possible.
        """
        @click.command(name=self.name, help=self.help_text)
        def the_command():
            click.echo(f"Raising window {self.pattern}")
            raise_window(self.pattern)

        return the_command


class WindowItemList(MenuItemList):
    """A persistable list of window items"""

    item_classes = [WindowItem]


class WindowRaiser(YeahYeahPlugin):
    def __init__(self, item_list):
        """Plugin can get windows into focus

        Parameters
        ----------
        item_list: WindowItemList

        """
        super().__init__(slug="window_raiser", short_slug='raiser')
        self.item_list = item_list
        self.config_file_path = None

    @classmethod
    def __from_file_path__(cls, config_file_path):
        cls.assert_config_file(config_file_path)
        with open(config_file_path, "r") as f:
            pattern_list = WindowItemList.load(f)

        obj = cls(item_list=pattern_list)
        obj.config_file_path = config_file_path
        return obj

    def save(self):
        """Save current pattern list to disk if possible"""
        if self.config_file_path:
            with open(self.config_file_path, 'w') as f:
                self.item_list.save(file=f)

    @staticmethod
    def assert_config_file(config_file_path):
        """Make sure config file exists. If not, create an example config file"""
        if config_file_path.exists():
            return
        else:
            config_file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(config_file_path, "w") as f:
                example_patterns = [
                    WindowItem(
                        name="slack",
                        pattern="slack",
                        help_text="Raises the window called 'slack'",
                    ),
                    WindowItem(
                        name="email",
                        pattern="gmail",
                        help_text="Raises the window called 'slack'",
                    )
                ]
                WindowItemList(items=example_patterns).save(f)
            click.echo(
                f"WindowRaises config file {config_file_path} did not exist. Creating with default contents.."
            )

    def get_menu_items(self):
        """

        Returns
        -------
        List[WindowItemList]
        """
        return self.item_list.items

    def get_admin_commands(self):
        """

        Returns
        -------
        List[click.Command]
            list of click commands that can be used to admin this plugin

        """

        @click.command()
        def status():
            """Print some info for this plugin"""
            status_str = f"WindowRaiserPlugin:\n" \
                         f"{len(self.get_menu_items())} path_items in plugin\n"
            if self.config_file_path:
                status_str += f"Config file: {self.config_file_path}"
            click.echo(status_str)

        @click.command()
        @click.argument('keyword')
        @click.argument('pattern')
        def add(keyword, pattern):
            """Add a new url pattern"""
            pattern = WindowItem(name=keyword, pattern=pattern)
            click.echo(f"Adding {pattern}")
            self.item_list.append(pattern)
            self.save()

        @click.command()
        @click.argument('keyword')
        def remove(keyword):
            """Remove an existing url pattern"""
            to_remove = [x for x in self.item_list if x.name == keyword]
            if not to_remove:
                click.echo(f"Pattern with keyword {keyword} not found")
            else:
                click.echo(f"Removing {[str(x) for x in to_remove]}")
                for x in to_remove:
                    self.item_list.remove(x)
                self.save()

        @click.command()
        def list():
            """list all url path_items"""
            click.echo("\n".join([str(x) for x in self.item_list]))

        return [status, list, add, remove]


def raise_window(name):
    """Raise the first windows that matches name. Uses xdotool

    Parameters
    ----------
    name: str
        name of window to raise. Can be partial match
    """

    if platform.system() == 'Linux':
        subprocess.call(args=f'xdotool search -name {name} windowactivate %@]'.split(' '))
    else:
        raise NotImplemented(f"Opening new terminal not supported on platform '{platform.system()}'")
