from asyncio.windows_events import NULL
from lab import errors
import csv
from lab import processing

pathCSV = ""

def printMenu():
    print("=====================================Меню=====================================\n")
    print("Команда --- Действие")
    print("   1    --- Загрузка из CSV файла")#загрузка из файла в кеш(список)
    print("   2    --- Сохранение в CSV файл")#сохранение в текущий файл
    print("   3    --- Показ всех студентов")#только имена
    print("   4    --- Добавление студента")#добавление в кеш(список)
    print("   5    --- Обновление оценки по ID и номеру самой оценки")
    print("   6    --- Удаление оценки по ID и номеру самой оценки")
    print("   7    --- Удаление по ID")#удаление из кеша(список)
    print("   8    --- Обновление оценок по ID")#сохранение в текущий файл, просто кеш(список) не очищается
    print("   9    --- Показ статистики по группе")#буквально вывод всех данных из кеша(список)
    print("   10   --- Экспорт ТОП-N студентов в CSV файл по среднему баллу")#создание нового файла
    print("   11   --- Сортировка по avg и показ результата")#сортировка в кеше(список)
    print("   12   --- Сортировка по name и показ результата")#сортировка в кеше(список)
    print("   13   --- Сортировка по ID и показ результата")#сортировка в кеше(список)
    print("   14   --- Выход из программы\n")
    print("==============================================================================")
def loadFromCSV():
    pathCSV = input("Введите полный путь CSV файла: \n")
    students = []
    try:
        with open(pathCSV.strip(), encoding='utf-8') as f:
            reader = csv.reader(f)
            row_size = -1
            lineNumber = -1
            int_field = -1
            for row in reader:
                if not row:
                    continue
                its_header = False
                lineNumber += 1
                index = -1
                id = ""
                name = ""
                grades = []
                for element in row:
                    if lineNumber == 0:
                        row_size += 1
                    index += 1
                    if index == 0:
                        id = element.strip()
                        if lineNumber == 0:
                            try:
                                int_field = int(id)
                            except ValueError:
                                if id == "id":
                                    its_header = True
                                else:
                                    raise errors.CSVError("Первое поле заголовка не id")
                    elif index == 1:
                        name = element.strip()
                        if its_header and name != "name":
                            raise errors.CSVError("Второе поле заголовка не name")
                    else:
                        if its_header:
                            if element.strip() != f"grade{index - 1}":
                                raise errors.CSVError(f"{row_size + 1} поле заголовка не grade{row_size - 1}")
                if not its_header:
                    if index != row_size:
                        raise errors.CSVError(f"В строке {lineNumber} не хватает данных")
                    students.append(row)
            return students
    except FileNotFoundError:
        print(f"Файл {pathCSV} не найден.")
        return NULL
    except PermissionError:
        print(f"Нет прав на чтение файла {pathCSV} или этот путь указывает на директорию.")
        return NULL
    except NotADirectoryError:
        print(f"Компонент пути {pathCSV} не является папкой.")
        return NULL
    except IsADirectoryError:
        print(f"Путь {pathCSV} указывает на папку, а не на файл CSV.")
        return NULL
    except UnicodeDecodeError:
        print(f"Ошибка декодирования файла {pathCSV}")
        return NULL
    except csv.Error:
        print("Ошибка встроенного парсера CSV")
        return NULL
    except StopIteration:
        print(f"Файл {pathCSV} пустой")
        return NULL
    except errors.CSVError as e:
        print(f"CSV файл {pathCSV} имеет неправильный формат: " + str(e))
        return NULL
    except errors.InvalidDataError as e:
        print(e)
        return NULL
def saveToCSV(students: processing.Students):
    if not students:
        print("Нет данных для сохранения")
    else:
        try:
            with open(pathCSV, 'w', encoding='utf-8', newline='') as f:
                header = ['id', 'name']
                for i in range(1, students.count_marks + 1):
                    header.append(f'grade{i}')
                writer = csv.writer(f)
                writer.writerow(header)
                for obj in students.students:
                    writer.writerow(obj.output())
                print("Данные сохранены в CSV файл")
        except FileNotFoundError:#это и есть та ошибка, которая появляется при открытии загрузке изменений в файл когда он открыт в ворде 
            print(f"Файл {pathCSV} не найден.")
        except PermissionError:
            print(f"Нет прав на чтение файла {pathCSV} или этот путь указывает на директорию.")
        except NotADirectoryError:
            print(f"Компонент пути {pathCSV} не является папкой.")
        except UnicodeDecodeError:
            print(f"Ошибка декодирования файла {pathCSV}")
        except IsADirectoryError:
            print(f"Путь {pathCSV} указывает на папку, а не на файл CSV.")
            return NULL
        except csv.Error:
            print("Ошибка встроенного парсера CSV")
            return NULL
def exportToCSV(students, pathCSV):
    if not students:
        print("Нет данных для сохранения")
    else:
        try:
            with open(pathCSV, 'w', encoding='utf-8', newline='') as f:
                header = ['id', 'name']
                for i in range(1, students[0].getMarksCount() + 1):
                    header.append(f'grade{i}')
                header.append("AVG")
                writer = csv.writer(f)
                writer.writerow(header)
                for obj in students:
                    writer.writerow(obj.output_with_AVG())
        except FileNotFoundError:
            print(f"Файл {pathCSV} не найден.")
        except PermissionError:
            print(f"Нет прав на чтение файла {pathCSV} или этот путь указывает на директорию.")
        except NotADirectoryError:
            print(f"Компонент пути {pathCSV} не является папкой.")
        except UnicodeDecodeError:
            print(f"Ошибка декодирования файла {pathCSV}")
        except IsADirectoryError:
            print(f"Путь {pathCSV} указывает на папку, а не на файл CSV.")
            return NULL
        except csv.Error:
            print("Ошибка встроенного парсера CSV")
            return NULL
