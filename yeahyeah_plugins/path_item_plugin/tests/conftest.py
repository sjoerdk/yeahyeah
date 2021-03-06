"""pytest fixtures shared by modules in this folder"""

import pytest
from click.testing import CliRunner

from yeahyeah_plugins.path_item_plugin.core import (
    PathItem,
    PathItemList,
    PathItemPlugin,
)
from yeahyeah.core import YeahYeah
from yeahyeah_plugins.url_pattern_plugin.core import (
    URLPatternList,
    UrlPattern,
    WildCardUrlPattern,
    UrlPatternsPlugin,
)


@pytest.fixture()
def url_pattern_list():
    """A pattern list with some content"""
    return URLPatternList(
        items=[
            UrlPattern(
                name="test1", pattern="https://host{pattern1}/something{pattern2}.php"
            ),
            UrlPattern(
                name="test2",
                pattern="https://athing.com",
                help_text="Another test pattern",
            ),
            WildCardUrlPattern(name="test5", pattern="https://search{query}"),
        ]
    )


@pytest.fixture()
def path_item_list():
    return PathItemList(
        items=[
            PathItem(
                name="home",
                path="/home/a_user/",
                help_text="(Example) Open home directory",
            ),
            PathItem(
                name="external_disk",
                path="/mnt/some_mount/user/something",
                help_text="(Example) Open that external disk",
            ),
        ]
    )


@pytest.fixture()
def yeahyeah_instance(url_pattern_list, path_item_list, tmpdir):
    """An instance of the yeahyeah launch manager with some default plugins_old and commands"""
    yeahyeah = YeahYeah(configuration_path=tmpdir)
    yeahyeah.add_plugin_instance(UrlPatternsPlugin(pattern_list=url_pattern_list))
    yeahyeah.add_plugin_instance(PathItemPlugin(item_list=path_item_list))

    return yeahyeah


class MockContextCliRunner(CliRunner):
    """A click.testing.CliRunner that always passes a mocked context to any call, making sure any operations
    on current dir are done in a temp folder
    """

    def __init__(self, *args, mock_context, **kwargs):

        super().__init__(*args, **kwargs)
        self.mock_context = mock_context

    def invoke(
        self,
        cli,
        args=None,
        input=None,
        env=None,
        catch_exceptions=True,
        color=False,
        mix_stderr=False,
        **extra
    ):
        return super().invoke(
            cli,
            args,
            input,
            env,
            catch_exceptions,
            color,
            mix_stderr,
            obj=self.mock_context,
        )


class YeahYeahCommandLineParserRunner(MockContextCliRunner):
    """A click runner that always injects a YeahYeahContext instance into the
    context
    """

    def __init__(self, *args, mock_context, **kwargs):
        """

        Parameters
        ----------
        mock_context: YeahYeahContext
        """
        super().__init__(*args, mock_context=mock_context, **kwargs)
