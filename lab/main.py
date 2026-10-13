from asyncio.windows_events import NULL
from lab import io_utils
from lab import processing
from lab import errors
import sys

def main():
    students = processing.Students()
    io_utils.printMenu()
    while True:
        action = input("Введите команду действия: ").strip()
        situation = True
        if action == "0":
            situation = False
            io_utils.printMenu()
        elif action == "1":
            try:
                students.clear()
                loaded = io_utils.loadFromCSV()
                if loaded != NULL:
                    for el in loaded:
                        students.addStudent(el)
                    print("Данные загружены из CSV файла")
                    students.state = True
            except errors.InvalidDataError as e:
                print(e)
        elif action == "2":
            if not students.state:
                print("Прежде чем сохранять данные, загрузите файл")
            else:
                io_utils.saveToCSV(students)
                students.clear()
                students.state = False
        elif action == "3":
            if not students.state:
                print("Прежде чем просматривать данные, загрузите файл")
            else:
                if students.is_empty():
                    print("Нет данных в кэше")
                else:
                    for i in range(len(students.students)):
                        print(students.students[i].name)
                    print("Все студенты показаны")
        elif action == "4":
            try:
                if not students.state:
                    raise errors.InvalidDataError("Прежде чем добавлять данные, загрузите файл")
                line = input("Введите данные о студенте через запятую: \n").strip()
                if not line:
                    raise errors.InvalidDataError("Вы ничего не ввели")
                info_student = line.split(',')
                students.addStudent(info_student)
                print("Студент добавлен")
            except errors.InvalidDataError as e:
                print(e)
        elif action == "5":
            try:
                if not students.state:
                    raise errors.InvalidDataError("Прежде чем обновлять данные, загрузите файл")
                if students.is_empty():
                    print("Оценку менять некому")
                else:
                    line = input("Введите ID студента, номер оценки и значение оценки через запятую: \n").strip()
                    if not line:
                        raise errors.InvalidDataError("Вы ничего не ввели")
                    info_student = line.split(',')
                    students.updateMark(info_student)
                    print("Оценка студента обновлена")
            except errors.InvalidDataError as e:
                print(e)
        elif action == "6":
            try:
                if not students.state:
                    raise errors.InvalidDataError("Прежде чем удалять данные, загрузите файл")
                if students.is_empty():
                    print("Оценку удалять некому")
                else:
                    line = input("Введите ID студента и номер оценки через запятую: \n").strip()
                    if not line:
                        raise errors.InvalidDataError("Вы ничего не ввели")
                    info_student = line.split(',')
                    students.delMark(info_student)
                    print("Оценка студента удалена")
            except errors.InvalidDataError as e:
                print(e)
        elif action == "7":
            try:
                if not students.state:
                    raise errors.InvalidDataError("Прежде чем удалять данные, загрузите файл")
                if students.is_empty():
                    print("Некого удалять")
                else:
                    id_del = input("Введите ID студента которого надо удалить: \n")
                    students.delStudentByID(id_del.strip())
                    print("Студент удалён по ID")
            except errors.InvalidDataError as e:
                print(e)
        elif action == "8":
            if not students.state:
                print("Прежде чем сохранять данные, загрузите файл")
            else:
                io_utils.saveToCSV(students)
                print("Оценки обновлены")
        elif action == "9":
            if not students.state:
                print("Прежде чем просматривать данные, загрузите файл")
            else:
                if students.is_empty():
                    print("Кэш пустой")
                else:
                    print(students.output())
                    print("Статистика по группе показана")
        elif action == "10":
            if not students.state:
                print("Прежде чем экспортировать данные, загрузите файл")
            else:
                line = input("Введите количество N и путь указывающий на файл, который следует создать и в который надо вывести эти данные: \n")
                if not line:
                    raise errors.InvalidDataError("Вы ничего не ввели")
                info_export = line.split(',')
                try:
                    if len(info_export) < 2:
                        raise errors.InvalidDataError("Вы ввели недостаточно данных")
                    if len(info_export) > 2:
                        raise errors.InvalidDataError("Вы ввели слишком много данных")
                    students.sortAVG()
                    io_utils.exportToCSV(students.getTopN(info_export[0].strip()), info_export[1].strip())
                    print("Экспор ТОП-N студентов в CSV файл по среднему баллу завершён")
                except errors.InvalidDataError as e:
                    print(e)
        elif action == "11":
            if not students.state:
                print("Прежде чем сортировать данные, загрузите файл")
            else:
                if students.is_empty():
                    print("Нет данных в кэше")
                else:
                    students.sortAVG()
                    print(students.output())
                    print("Показаны студенты отсортированные по avg")
        elif action == "12":
            if not students.state:
                print("Прежде чем сортировать данные, загрузите файл")
            else:
                if students.is_empty():
                    print("Нет данных в кэше")
                else:
                    students.sortName()
                    print(students.output())
                    print("Показаны студенты отсортированные по name")
        elif action == "13":
            if not students.state:
                print("Прежде чем сортировать данные, загрузите файл")
            else:
                if students.is_empty():
                    print("Нет данных в кэше")
                else:
                    students.sortID()
                    print(students.output())
                    print("Показаны студенты отсортированные по ID")
        elif action == "14":
            sys.exit()
        else:
            print("Команда введена неверно или её не существует")
        if situation:
            print("   0    --- Открыть меню")
            print("   14   --- Выход из программы")

if __name__ == "__main__":
    main()
