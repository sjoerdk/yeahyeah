from functools import wraps

from click.exceptions import ClickException
from umcnad.exceptions import UMCNADException


def handle_umcnad_exceptions(func):
    """Convert any umcnad exceptions to click exceptions"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except UMCNADException as e:
            raise ClickException(f"Error in umcnad: {e}")

    return wrapper
