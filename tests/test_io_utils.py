import pytest
import csv
from lab import io_utils
from lab.models import Student

def test_print_menu(capsys):
    io_utils.printMenu()
    captured = capsys.readouterr()
    assert "==========Меню==========" in captured.out
    assert "Команда --- Действие" in captured.out
    assert "1    --- Загрузка из CSV файла" in captured.out
    assert "2    --- Сохранение в CSV файл" in captured.out
    assert "3    --- Показ всех студентов" in captured.out
    assert "4    --- Добавление студента" in captured.out
    assert "5    --- Обновление оценки по ID и номеру самой оценки" in captured.out
    assert "6    --- Удаление оценки по ID и номеру самой оценки" in captured.out
    assert "7    --- Удаление по ID" in captured.out
    assert "8    --- Обновление оценок по ID" in captured.out
    assert "9    --- Показ статистики по группе" in captured.out
    assert "10   --- Экспорт ТОП-N студентов в CSV файл по среднему баллу" in captured.out
    assert "11   --- Сортировка по avg и показ результата" in captured.out
    assert "12   --- Сортировка по name и показ результата" in captured.out
    assert "13   --- Сортировка по ID и показ результата" in captured.out
    assert "14   --- Выход из программы" in captured.out
    assert "========================" in captured.out

def test_load_from_csv_success(tmp_path, monkeypatch):
    csv_file = tmp_path / "group.csv"
    rows = [
        ["id", "name", "grade1", "grade2"],
        ["1", "Иван Иванов", "80", "90"],
        ["2", "Петр Петров", "70", " "]
    ]
    with open(csv_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    monkeypatch.setattr("builtins.input", lambda _: str(csv_file))
    load_result = io_utils.loadFromCSV()
    assert load_result == [["1", "Иван Иванов", "80", "90"], ["2", "Петр Петров", "70", " "]]

@pytest.mark.parametrize("bad_header", [
    ([["not_id", "name", "grade1"]]),
    ([["id", "not_name", "grade1"]]),
    ([["id", "name", "wrong_grade"]])
])
def test_load_from_csv_header_errors(tmp_path, monkeypatch, bad_header):
    csv_file = tmp_path / "bad_headers.csv"
    with open(csv_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(bad_header)
    monkeypatch.setattr("builtins.input", lambda _: str(csv_file))
    result = io_utils.loadFromCSV()
    assert result == io_utils.NULL

def test_export_to_csv_correct_format(tmp_path):
    export_file = tmp_path / "top_export.csv"
    students_list = [
        Student("1", "Студент Тестов", ["100", "80"])
    ]
    io_utils.exportToCSV(students_list, str(export_file))
    with open(export_file, "r", encoding="utf-8") as f:
        file_content = list(csv.reader(f))
        assert file_content[0] == ["id", "name", "grade1", "grade2", "AVG"]
        assert file_content[1] == ["1", "Студент Тестов", "100", "80", "90.0"]
