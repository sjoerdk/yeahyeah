from click import ClickException
from clockifyclient.exceptions import ClockifyClientException


def handle_clockify_exceptions(func):
    """Convert any clockify api exceptions to click exceptions"""

    def decorated(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ClockifyClientException as e:
            raise ClickException(f"Error in Clockify API: {e}")

    return decorated




