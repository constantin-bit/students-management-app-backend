import pytest
from lab import main

def test_main_loop_exit_command(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "14")
    with pytest.raises(SystemExit):
        main.main()

def test_main_invalid_command_warning(monkeypatch, capsys):
    commands = iter(["99", "14"])
    monkeypatch.setattr("builtins.input", lambda _: next(commands))
    with pytest.raises(SystemExit):
        main.main()
    captured = capsys.readouterr()
    assert "Команда введена неверно или её не существует" in captured.out

def test_main_show_menu_zero_command(monkeypatch, capsys):
    commands = iter(["0", "14"])
    monkeypatch.setattr("builtins.input", lambda _: next(commands))
    with pytest.raises(SystemExit):
        main.main()
    captured = capsys.readouterr()
    assert captured.out.count("==========Меню==========") >= 2
