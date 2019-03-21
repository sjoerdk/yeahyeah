import subprocess

import click
import yaml

from yeahyeah.core import YeahYeahMenuItem, YeahYeahPlugin


class PathItem(YeahYeahMenuItem):
    """A named UNC path"""

    def __init__(self, name, path, help_text=None):
        super().__init__(name, help_text)
        self.path = path

    def __str__(self):
        return f"PathItem {self.name}:{self.path}"

    @property
    def help_text(self):
        if self._help_text is None:
            return f"open {self.path}"
        else:
            return self._help_text

    def to_click_command(self):
        """This url pattern as a click command that can be added with add_command()
        """

        @click.command(name=self.name, help=self.help_text)
        def the_command():
            click.echo(f"jumping to {self.path}")
            command = f'konsole -e bash --init-file <(echo ". \\\"$HOME/.bashrc\\\"; cd {self.path}")'
            click.echo(f"executing {command}")
            subprocess.run(command, shell=True)

        return the_command

    @classmethod
    def to_yaml(cls, dumper, obj):
        """Dump to yaml as dictionary"""
        return dumper.represent_dict(obj.to_dict())

    def to_dict(self):
        """Represent this UrlPattern as a dictionary:

        """
        values = {"path": self.path}
        if self._help_text is not None:
            values["text"] = self._help_text
        return {self.name: values}

    @staticmethod
    def from_dict(dict_in):
        """Create a UrlPattern object from given dict.

        Dict should have been created with to_dict()
        """
        name = list(dict_in.keys()).pop()
        values = dict_in[name]
        path = values["path"]
        help_text = values.get("text", None)

        return PathItem(name=name, path=path, help_text=help_text)



class PathItemList:
    """A persistable list of path items"""

    def __init__(self, path_items):
        """

        Parameters
        ----------
        path_items: List[PathItem]
        """
        self.path_items = path_items

    def save(self, file):
        """Save list to file

        Parameters
        ----------
        file: Open file handle
            save to this file

        Returns
        -------

        """
        yaml.dump(self.to_dict(), file, default_flow_style=False)

    def append(self, item):
        self.path_items.append(item)

    def __iter__(self):
        return self.path_items.__iter__()

    def __len__(self):
        return self.path_items.__len__()

    def remove(self, item):
        return self.path_items.remove(item)

    def to_dict(self):
        """This URLPatternList as dict, as terse as possible:

        {pattern_name1: {param1: value1,...},
         pattern_name2: {param2: value2,...},
        """
        result = {}
        for pattern in self.path_items:
            pattern_dict = pattern.to_dict()
            result.update(pattern_dict)

        return result

    @staticmethod
    def load(file):
        """Try to load a UrlPatternList from file handle

        Parameters
        ----------
        file: open file hanle

        Returns
        -------
        URLPatternList

        Raises
        ------
        TypeError:
            When object loaded is not a list


        """
        loaded = yaml.load(file)

        if type(loaded) is not dict:
            msg = f"Expected to load a dictionary, but found {type(loaded)} instead"
            raise TypeError(msg)
        # flatten to list of dicts
        pattern_list = []
        for key, values in loaded.items():
            pattern_list.append(PathItem.from_dict({key: values}))

        return PathItemList(path_items=pattern_list)


class PathItemPlugin(YeahYeahPlugin):
    def __init__(self, item_list):
        """Plugin that holds PathItems

        Parameters
        ----------
        item_list: PathItemList

        """
        super().__init__(slug="path_items")
        self.item_list = item_list
        self.config_file_path = None

    @classmethod
    def __from_file_path__(cls, config_file_path):
        cls.assert_config_file(config_file_path)
        with open(config_file_path, "r") as f:
            item_list = PathItemList.load(f)

        obj = cls(item_list=item_list)
        obj.config_file_path = config_file_path
        return obj

    def save(self):
        """Save current list to disk if possible"""
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
                    PathItem(
                        name="home",
                        path="/home/a_user/",
                        help_text="(Example) Open home directory",
                    ),
                    PathItem(
                        name="external_disk",
                        path="/mnt/some_mount/user/something",
                        help_text="(Example) Open that external disk",
                    )
                ]
                PathItemList(path_items=example_patterns).save(f)
            click.echo(
                f"PathItem config file {config_file_path} did not exist. Creating with default contents.."
            )

    def get_menu_items(self):
        """

        Returns
        -------
        List[UrlPattern]
        """
        return self.item_list.path_items

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
            status_str = f"PathItemPlugin:\n" \
                         f"{len(self.get_menu_items())} path items in plugin\n"
            if self.config_file_path:
                status_str += f"Config file: {self.config_file_path}"
            click.echo(status_str)

        @click.command()
        @click.argument('keyword')
        @click.argument('pattern')
        def add(keyword, path):
            """Add a new url pattern"""
            pattern = PathItem(name=keyword, path=path)
            click.echo(f"Adding {pattern}")
            self.item_list.append(pattern)
            self.save()

        @click.command()
        @click.argument('keyword')
        def remove(keyword):
            """Remove an existing path item"""
            to_remove = [x for x in self.item_list if x.name == keyword]
            if not to_remove:
                click.echo(f"path with keyword {keyword} not found")
            else:
                click.echo(f"Removing {[str(x) for x in to_remove]}")
                for x in to_remove:
                    self.item_list.remove(x)
                self.save()

        @click.command()
        def list():
            """list all paths"""
            click.echo("\n".join([str(x) for x in self.item_list]))

        return [status, list, add, remove]
