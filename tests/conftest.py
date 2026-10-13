import pytest
from lab.models import Student

@pytest.fixture
def valid_student_data():
    return ["  1 ", "    Иванов Иван ", ["  80 ", "90  ", " 100"]]

@pytest.fixture
def sample_student():
    return Student("2", "Петров Петр", ["70", " ", "90"])