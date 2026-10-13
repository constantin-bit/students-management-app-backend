import pytest
from lab.models import Student
from lab.errors import InvalidDataError

def test_student_successful_creation(valid_student_data):
    student = Student(valid_student_data[0], valid_student_data[1], valid_student_data[2])
    assert student.id == 1
    assert student.name == "Иванов Иван"
    assert student.grades == [80, 90, 100]
    assert student.marks_count == 3

@pytest.mark.parametrize("bad_id", ["-5", "0", "abc", "", "   "])
def test_student_invalid_id(bad_id):
    with pytest.raises(InvalidDataError):
        Student(bad_id, "Жмыг Жмыгович", ["100"])

@pytest.mark.parametrize("bad_name", ["", "   "])
def test_student_invalid_name(bad_name):
    with pytest.raises(InvalidDataError):
        Student("1", bad_name, ["0"])

def test_student_invalid_grades_type():
    with pytest.raises(InvalidDataError):
        Student("1", "Альберт", "not_a_list")

@pytest.mark.parametrize("bad_grades", [
    ["105", "50"], 
    ["-5", "20"], 
    ["abc"]
])
def test_student_invalid_grades_values(bad_grades):
    with pytest.raises(InvalidDataError):
        Student("1", "Осёл", bad_grades)

def test_student_output_formats(sample_student):
    assert sample_student.output() == ["2", "Петров Петр", "70", " ", "90"]
    assert sample_student.output_with_AVG() == ["2", "Петров Петр", "70", " ", "90", "80.0"]

def test_student_change_and_delete_mark(sample_student):
    sample_student.changeMark(2, 85)
    assert sample_student.grades[1] == 85
    sample_student.delMark(1)
    assert sample_student.grades[0] == -100

def test_student_average_calculation():
    student = Student("1", "Студент", ["80", " ", "90"])
    assert student.getAverage() == 85.0

def test_student_average_empty_grades():
    student = Student("1", "Студент", [" ", " "])
    assert student.getAverage() == 0

def test_student_gets(sample_student):
    assert sample_student.getID() == 2
    assert sample_student.getName() == "Петров Петр"
    assert sample_student.getMarksCount() == 2