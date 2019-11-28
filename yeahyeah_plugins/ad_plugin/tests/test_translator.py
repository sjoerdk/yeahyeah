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


@pytest.fixture()
def some_other_text():
    return """
        job 53781 on p01:
        
        ('job_id', 53781)
        ('date', '2019-10-24T12:11:10')
        ('user_name', 'z123456')
        ('status', 'DONE')
        ('error', None)
        ('description', '{User: UMCN\\z123456}{RequestKey: 418}')
        ('project_name', 'Cliniquest')
        ('priority', 4)
        ('files_downloaded', 3289)
        ('files_processed', 3288)
        ('destination_id', 53779)
        ('destination_name', None)
        ('destination_path', '\\\\umcsanfsclp01\\radng_idis_out\\Z123456\\cliniquestTEST8_V4')
        ('destination_network', None)
        ('destination_status', 'BASE')
        ('destination_type', 'PATH')
        ('source_id', 53779)
        ('source_instance_id', 'accession_number:1356676.23557070')
        ('source_status', 'NEW')
        ('source_type', 'WADO')
        ('source_anonymizedpatientid', None)
        ('source_anonymizedpatientname', None)
        ('source_pims_keyfile_id', 39)
        ('source_name', 'IDC_WADO')
        ('source_path', None)
        ('source_protocol', 3178)
        ('source_subject', 3178)

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


def test_z_translator_tricky_text(some_other_text, person_list):
    """Try replacing with lots of special chars"""
    persons: List[UMCNPerson] = person_list
    glossary = {x.z_number: str(x) for x in persons}

    result = Translator(glossary).process(some_other_text)
    assert result.count("Testo, Jane") == 3

