import pytest
from umcnad.core import UMCNPerson


@pytest.fixture()
def person_list():
    return [
        UMCNPerson(
            z_number="z123456",
            full_name="Testo, Jane",
            email="jane.testo@umcn.nl",
            department="test department A",
        ),
        UMCNPerson(
            z_number="z123457",
            full_name="Testguy, Jack, ",
            email="jack.testguy@umcn.nl",
            department="test department B",
        ),
    ]
