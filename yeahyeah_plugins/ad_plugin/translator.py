import re
from typing import Dict


class Translator:
    """Replaces strings with other strings
    """

    def __init__(self, glossary: Dict[str, str], ignore_case=True):
        self.glossary = glossary
        self.ignore_case = ignore_case

    def get_expressions(self):
        if self.ignore_case:
            def re_compile(x):
                return re.compile(re.escape(x), re.IGNORECASE)
        else:
            def re_compile(x):
                return re.compile(re.escape(x))

        return {re_compile(org): new
                for org, new in self.glossary.items()}

    def process(self, string_in):
        current = string_in
        for expression, new in self.get_expressions().items():
            current = expression.sub(new, current)
        return current


def find_z_numbers(string_in):
    """Find any unique substring that looks like a z-number

    Parameters
    ----------
    string_in: str
        Any string

    Returns
    -------
    List[str]
        Uppercase version of each unique z-number found in the text
    """

    z_numbers = re.compile('z[0-9]{6}', re.IGNORECASE).findall(string_in)
    z_numbers = list(set([x.upper() for x in z_numbers]))  # remove duplicates
    return z_numbers
