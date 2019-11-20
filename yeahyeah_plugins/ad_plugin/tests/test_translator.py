from typing import Dict, List

import pytest
from umcnad.core import UMCNPerson

from yeahyeah_plugins.ad_plugin.translator import Translator, find_z_numbers


@pytest.fixture()
def some_text():
    return """
        55184  2019-11-15T11:57:15  DONE     4          2          z690133        
        55182  2019-11-15T11:54:03  DONE     1858       1850       z690133        
        55179  2019-11-14T16:47:03  DONE     2235       2234       z123456
        55173  2019-11-13T14:31:26  DONE     2028       2028       z123457
        55172  2019-11-08T13:32:38  ERROR    None       None       z690133        
    """


def test_translator():
    glossary = {"Jack": "Jaap", "Anne": "Annelies"}
    translator = Translator(glossary)
    assert translator.process("And jack went") == "And Jaap went"
    assert translator.process("And jacko went") == "And Jaapo went"
    assert translator.process("And annejacko went") == "And AnneliesJaapo went"

    translator = Translator(glossary, ignore_case=False)
    assert translator.process("And jack went") == "And jack went"


def test_find_z_numbers(some_text):

    assert all(
        x in ["Z123457", "Z690133", "Z123456"] for x in find_z_numbers(some_text)
    )
    assert find_z_numbers("") == []


def test_z_translator(some_text, person_list):
    """Replace z-numbers with person names in text """
    z_numbers = find_z_numbers(some_text)
    # persons = find_persons(z_numbers)
    persons: List[UMCNPerson] = person_list
    glossary = {x.z_number: str(x) for x in persons}
    expected = """
        55184  2019-11-15T11:57:15  DONE     4          2          z690133        
        55182  2019-11-15T11:54:03  DONE     1858       1850       z690133        
        55179  2019-11-14T16:47:03  DONE     2235       2234       Testo, Jane (z123456)
        55173  2019-11-13T14:31:26  DONE     2028       2028       Testguy, Jack,  (z123457)
        55172  2019-11-08T13:32:38  ERROR    None       None       z690133        
    """
    assert Translator(glossary).process(some_text) == expected


