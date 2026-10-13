import pytest
from lab.processing import Students
from lab.errors import InvalidDataError

@pytest.fixture
def students_manager():
    return Students()

def test_add_student_success(students_manager):
    """Успешное базовое добавление студента в менеджер."""
    students_manager.addStudent(["1", "Алексей", "90", "80"])
    assert len(students_manager.students) == 1
    assert students_manager.count_marks == 2
    assert 1 in students_manager.all_ID

def test_add_student_insufficient_data(students_manager):
    """Передана строка, где меньше 3 элементов."""
    with pytest.raises(InvalidDataError):
        students_manager.addStudent(["1", "Алексей"])

def test_add_student_different_marks_count(students_manager):
    """Попытка добавить студента, у которого кол-во оценок не совпадает с группой."""
    students_manager.addStudent(["1", "Алексей", "90", "80"])
    assert students_manager.count_marks == 2
    with pytest.raises(InvalidDataError):
        students_manager.addStudent(["2", "Глаз", "100"])

def test_add_student_duplicate_id(students_manager):
    """Проверка защиты от добавления двух студентов с одинаковым ID."""
    students_manager.addStudent(["1", "Алексей", "90"])
    with pytest.raises(InvalidDataError):
        students_manager.addStudent(["1", "Кружка", "80"])

@pytest.mark.parametrize("bad_id", ["-1", "abc", "999"])
def test_delete_student_exceptions(students_manager, bad_id):
    """Проверка обработки всех ошибочных сценариев при удалении ID."""
    students_manager.addStudent(["1", "Алексей", "90"])
    with pytest.raises(InvalidDataError):
        students_manager.delStudentByID(bad_id)

def test_delete_student_by_id_success(students_manager):
    """Проверка успешного удаления студента по его ID."""
    students_manager.addStudent(["5", "Дмитрий", "90"])
    students_manager.delStudentByID("5")
    assert len(students_manager.students) == 0
    assert 5 not in students_manager.all_ID

@pytest.mark.parametrize("bad_updating_parametrs", [
    ["1","1"], ["1","1","80","90"],
    ["abc","1","80"], ["","1","80"], ["-7","1","80"], ["7","1","80"],
    ["1","abc","80"], ["1","","80"], ["1","-7","80"], ["1","7","80"],
    ["1","1","abc"], ["1","1",""], ["1","1","-2"], ["1","1","180"],
    ])
def test_updating_mark(students_manager, bad_updating_parametrs):
    students_manager.addStudent(["1", "Иван", "60", "40"])
    with pytest.raises(InvalidDataError):
        students_manager.updateMark(bad_updating_parametrs)

@pytest.mark.parametrize("bad_deleting_parametrs", [
    ["1"], ["1","1","80"],
    ["abc","1"], ["","1"], ["-7","1"], ["7","1"],
    ["1","abc"], ["1",""], ["1","-7"], ["1","7"]
    ])
def test_updating_mark(students_manager, bad_deleting_parametrs):
    students_manager.addStudent(["1", "Иван", "60", "40"])
    with pytest.raises(InvalidDataError):
        students_manager.delMark(bad_deleting_parametrs)

@pytest.mark.parametrize("bad_n", ["-1", "abc", "999"])
def test_manager_sorting_and_top_n(students_manager, bad_n):
    """Комплексный тест сортировок по разным критериям и среза Top-N."""
    students_manager.addStudent(["3", "Влад", "100"])
    students_manager.addStudent(["1", "Анна", "50"])
    students_manager.addStudent(["2", "Борис", "80"])
    students_manager.sortID()
    assert [s.id for s in students_manager.students] == [1, 2, 3]
    students_manager.sortName()
    assert [s.name for s in students_manager.students] == ["Анна", "Борис", "Влад"]
    students_manager.sortAVG()
    assert [s.id for s in students_manager.students] == [3, 2, 1]
    with pytest.raises(InvalidDataError):
        top2 = students_manager.getTopN(bad_n)
    top_2 = students_manager.getTopN("2")
    assert len(top_2) == 2
    assert top_2[0].id == 3
    assert top_2[1].id == 2

def test_output_students(students_manager):
    students_manager.addStudent(["3", "Влад", "100", ""])
    students_manager.addStudent(["1", "Анна", "50", "70"])
    assert students_manager.output() == "3, Влад, 100,  \n1, Анна, 50, 70\n"
    assert students_manager.outputTopN(1) == "3, Влад, 100,  \n"

def test_empty_clear_students(students_manager):
    assert students_manager.is_empty() == True
    students_manager.addStudent(["3", "Влад", "100", ""])
    assert students_manager.is_empty() == False
    students_manager.clear()
    assert students_manager.is_empty() == True