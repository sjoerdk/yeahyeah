import datetime

import click

from clockify_plugin.context import ClockifyPluginContext, pass_clockify_context, default_context
from clockify_plugin.context import default_settings_file_name
from yeahyeah.core_new import YeahYeahContext, pass_yeahyeah_context
from yeahyeah.persistence import JSONSettingsFile


@click.group(name="log")
@click.pass_context
@pass_yeahyeah_context
def main(context: YeahYeahContext, ctx):
    """write log"""
    settings_file = JSONSettingsFile(path=context.settings_path / default_settings_file_name)
    if not settings_file.exists():
        click.echo(f"Settings file not found. Writing default settings to {settings_file.path}")
        settings_file.save(dict_in=default_context.to_dict())
    ctx.obj = ClockifyPluginContext.init_from_dict(settings_file.load())


@click.command()
@pass_clockify_context
def status(context: ClockifyPluginContext):
    """Show server and api key"""
    click.echo(f"Using api key {context.api_key} with clockify server '{context.api_url}'")


@click.command()
@pass_clockify_context
@click.argument("message", nargs=-1)
@click.option("-p", "--project", type=str)
@click.option(
    "-t",
    "--timedelta",
    type=int,
    default=0,
    help="minutes to add or subtract to now() for start of log",
)
def add(context: ClockifyPluginContext, message, project, timedelta):
    """add log message"""
    if not message:
        click.echo("Log message may not be empty")
        return
    log_start = datetime.datetime.utcnow() + datetime.timedelta(minutes=timedelta)
    #self.clockify_session.add_time_entry()
    click.echo(f"Adding {' '.join(message)} at {log_start} to project {project}")


@click.command()
@pass_clockify_context
def stop(context: ClockifyPluginContext):
    """stop any active logging stopwatch"""
    click.echo(f"Stopping")


@click.command()
@pass_clockify_context
def projects(context: ClockifyPluginContext):
    """Lists available projects for current clockify user"""
    click.echo(f"Projects")


for func in [status, add, stop, projects]:
    main.add_command(func)


@click.command()
@pass_yeahyeah_context
def edit_settings(context: YeahYeahContext):
    """Open settings file for editing"""
    click.launch(str(context.settings_path / default_settings_file_name))
