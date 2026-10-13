import pytest
import csv
from lab import main
from lab import io_utils

def test_app_complete_user_workflow(tmp_path, monkeypatch, capsys):
    source_file = tmp_path / "students_database.csv"
    initial_data = [
        ["id", "name", "grade1"],
        ["7", "Петрович", "75"]
    ]
    with open(source_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(initial_data)
    io_utils.pathCSV = str(source_file)
    user_session_steps = iter([
        "1",                    #Загрузка файла
        str(source_file),       #Пишем путь к файлу
        "3",                    #Просмотр всех — должен быть Петрович
        "4",                    #Добавление нового студента
        "12, Иванов Иван, 98",  #Вводим данные через запятую
        "3",                    #Просматриваем, что Иванов Иван появилась в списке рядом с Петровичем
        "14"                    #Выход из программы
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(user_session_steps))
    with pytest.raises(SystemExit):
        main.main()
    console_output = capsys.readouterr().out
    assert "Данные загружены из CSV файла" in console_output
    assert "Петрович" in console_output
    assert "Студент добавлен" in console_output
    assert "Петрович" in console_output
    assert "Иванов Иван" in console_output
    assert "Все студенты показаны" in console_output
