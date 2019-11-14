import click

from yeahyeah.decorators import pass_yeahyeah_context
from yeahyeah.context import YeahYeahContext
from yeahyeah.persistence import JSONSettingsFile
from yeahyeah_plugins.ad_plugin.context import default_settings_file_name, \
    default_context, ADPluginContext, pass_ad_context
from yeahyeah_plugins.ad_plugin.decorators import handle_umcnad_exceptions


@click.group(name="ad")
@click.pass_context
@pass_yeahyeah_context
def main(context: YeahYeahContext, ctx):
    """Query Active Directory"""
    settings_file = JSONSettingsFile(
        path=context.settings_path / default_settings_file_name
    )
    if not settings_file.exists():
        click.echo(
            f"Settings file not found. Writing default context to {settings_file.path}"
        )
        settings_file.save(dict_in=default_context.to_dict())
    ctx.obj = ADPluginContext.init_from_dict(settings_file.load())


@click.command()
@pass_ad_context
def status(context: ADPluginContext):
    """Show server and api key"""
    click.echo(f"hello {context}")


@click.command()
@handle_umcnad_exceptions
@pass_yeahyeah_context
def edit_settings(context: YeahYeahContext):
    """Open context file for editing"""
    click.launch(str(context.settings_path / default_settings_file_name))


for func in [status]:
    main.add_command(func)
