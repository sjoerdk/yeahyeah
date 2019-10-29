"""Migrating to a better way of using click.
Old way:  Generate all click functions inside classes and kind of hack in the 'self' object by attaching the class self
to the generated functions, like this:

class plugin:

    def get_click_command(self):

        @click.command()
        def a_command():
            self.do_thing()  # self is kind of strangely inserted here

        return a_command


The new way is to use proper click command interleaving with pass_context() and passing around settings objects:

@click.command()
@click.pass_context
def a_command(ctx):
    ctx.do_thing()


This makes the code less convoluted, more testable and more separated.


However I can't do all this refactoring in one go. Time constraints. So doing this step by step. Anything in the new
scheme gets moved here to core_new.py When refactoring is complete this gets renamed to core.py
"""
import click


class YeahYeahContext:
    """Core yeahyeah context object. This gets passed to all plugins by default when calling any plugin method

    """
    def __init__(self, settings_path):
        """

        Parameters
        ----------
        settings_path: Pathlike
            Path to the folder where any settings can be stored
        """
        self.settings_path = settings_path


pass_yeahyeah_context = click.make_pass_decorator(YeahYeahContext)


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


