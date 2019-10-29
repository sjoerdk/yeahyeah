import datetime
import json

import click
from clockifyclient.api import APIServer
from clockifyclient.client import APISession
from dateutil import tz

from yeahyeah.core import (
    YeahYeahGeneratorPlugin,
    SerialisableMenuItem,
    MenuItemList,
    YeahYeahMenuItem,
)


class ClockifyPluginSettings:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    @classmethod
    def init_from_dict(cls, dict_in):
        return cls(api_key=dict_in["api_key"], api_url=dict_in["api_url"])

    def to_dict(self):
        return {"api_key": self.api_key, "api_url": self.api_url}


class ClockifyPlugin(YeahYeahGeneratorPlugin):

    def __init__(self, api_url, api_key, config_file_path=None):
        """Plugin that controls clockify

        Parameters
        ----------
        api_url: str
            full path to clockify api
        api_key: str
            api key to identify yourself
        config_file_path: str, optional
            config path to save to

        """
        super().__init__(slug="clockify", short_slug="clock")
        self.api_url = api_url
        self.api_key = api_key
        self.config_file_path = config_file_path
        self.clockify_session = APISession(
            api_server=APIServer(self.api_url), api_key=self.api_key
        )

    @classmethod
    def __from_file_path__(cls, config_file_path):
        cls.assert_config_file(config_file_path)
        with open(config_file_path, "r") as f:
            settings = ClockifyPluginSettings.init_from_dict(json.loads(f.read()))
        return cls(
            api_key=settings.api_key,
            api_url=settings.api_url,
            config_file_path=config_file_path,
        )

    @staticmethod
    def assert_config_file(config_file_path):
        """Make sure config file exists. If not, create an example config file"""
        if config_file_path.exists():
            return
        else:
            config_file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(config_file_path, "w") as f:
                settings = ClockifyPluginSettings(
                    api_key="<your clockify api key>",
                    api_url="https://api.clockify.me/api/v1",
                )
                f.write(json.dumps(settings.to_dict()))
            click.echo(
                f"Clockify config file {config_file_path} did not exist. Creating with default contents.."
            )

    def get_commands(self):
        """

        Returns
        -------
        List[YeahYeahMenuItem]
        """

        @click.group()
        def log():
            """write log"""
            pass

        @click.command()
        @click.argument("message", nargs=-1)
        @click.option("-p", "--project", type=str)
        @click.option(
            "-t",
            "--timedelta",
            type=int,
            default=0,
            help="minutes to add or subtract to now() for start of log",
        )
        def add(message, project, timedelta):
            """add log message"""
            if not message:
                click.echo("Log message may not be empty")
                return
            log_start = datetime.datetime.utcnow() + datetime.timedelta(minutes=timedelta)
            #self.clockify_session.add_time_entry()
            click.echo(f"Adding {' '.join(message)} at {log_start} to current workspace {project}")

        @click.command()
        def stop():
            """stop any active logging stopwatch"""
            click.echo(f"Stopping")

        @click.command()
        def projects():
            """Lists available projects for current clockify user"""
            click.echo(f"Projects")

        log.add_command(add)
        log.add_command(stop)

        return [log]

    def get_admin_commands(self):
        """

        Returns
        -------
        List[click.Command]
            list of click commands that can be used to admin this plugin

        """

        @click.command()
        def edit_settings():
            """Open settings file for editing"""
            click.launch(str(self.config_file_path))

        return [edit_settings]
