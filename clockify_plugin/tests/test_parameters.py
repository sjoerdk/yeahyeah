from datetime import datetime

import click
import dateutil
import pytest

from clockify_plugin.parameters import TIME


def to_time_string(x):
    if not x:
        return None
    return x.strftime("%H:%M")


@pytest.fixture()
def fake_now_time(monkeypatch):
    monkeypatch.setattr(
        "clockify_plugin.parameters.now_local",
        lambda: datetime(
            year=2010,
            month=1,
            day=1,
            hour=6,
            minute=0,
            second=1,
            microsecond=0,
            tzinfo=dateutil.tz.gettz('Asia/Irkutsk'),
        ),
    )


@pytest.mark.parametrize(
    "input, expected_output",
    [
        (None, None),
        ("14:34", "14:34"),
        ("03:12", "03:12"),
        ("+1:02", "07:02"),
        ("-2:15", "03:45"),
        ("-15", "05:45"),
        ("+30", "06:30"),
        ("+01:19", "07:19"),
        ("-0:10", "05:50"),
        ("+120", "08:00"),
        ("+24:01", "06:01"),
        ("+0:120", "08:00"),
    ],
)
def test_time(fake_now_time, input, expected_output):
    """Test acceptable inputs"""
    assert (
        to_time_string(TIME.convert(value=input, param=None, ctx=None))
        == expected_output
    )


@pytest.mark.parametrize("input", ["skeuf", "+", "45:34", " "])
def test_exceptions(fake_now_time, input):
    """Test unacceptable input"""
    with pytest.raises(click.exceptions.BadParameter):
        to_time_string(TIME.convert(value=input, param=None, ctx=None))
