"""pytest fixtures shared by modules in this folder

"""
import pytest

from yeahyeah.core import YeahYeah
from yeahyeah.url_pattern import URLPatternList, UrlPattern, WildCardUrlPattern, UrlPatternsPlugin


@pytest.fixture()
def url_pattern_list():
    """A pattern list with some content"""
    return URLPatternList(
        patterns=[
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
def yeahyeah_instance(url_pattern_list):
    """An instance of the yeahyeah launch manager with some default plugins and commands"""
    yeahyeah = YeahYeah()
    plugin = UrlPatternsPlugin(pattern_list=url_pattern_list)
    yeahyeah.add_plugin(plugin)
    return yeahyeah
