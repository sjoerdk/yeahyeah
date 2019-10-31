import click

from yeahyeah.context import YeahYeahContext


def receives_yeahyeah_context(**kwargs):
    """Decorator for a click command that receives a YeahYeahContext object.

    Identical to

    @click.command(**kwargs)
    @click.pass_yeahyeah_context

    Just to prevent duplicated code
    """

    def decorator(func):
        return click.command(**kwargs)((pass_yeahyeah_context(func)))

    return decorator


pass_yeahyeah_context = click.make_pass_decorator(YeahYeahContext)
