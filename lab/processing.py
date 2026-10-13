from lab import models
from lab import errors

class Students:
    def __init__(self):
        self.state = False
        self.students = []
        self.count_marks = 0
        self.all_ID = set()
    def addStudent(self, student_data):
        if len(student_data) < 3:
            raise errors.InvalidDataError("Слишком мало данных о студенте")
        grades = student_data[2:]
        if self.count_marks == 0:
            self.count_marks = len(grades)
        else:
            if len(grades) != self.count_marks:
                raise errors.InvalidDataError("Слишком мало данных о студенте")
        student = models.Student(student_data[0].strip(), student_data[1].strip(), grades)
        if int(student_data[0].strip()) not in self.all_ID:
            self.students.append(student)
            self.all_ID.add(int(student_data[0].strip()))
        else:
            raise errors.InvalidDataError("Обнаружены одинаковые ID у студентов")
    def delStudentByID(self, id_student):
        try:
            id = int(id_student)
            if id <= 0:
                raise errors.InvalidDataError("Введёный ID не может быть отрицательным")
        except ValueError:
            raise errors.InvalidDataError("ID должен быть положительным целым числом")
        if id in self.all_ID:
            for index, el in enumerate(self.students):
                if el.id == id:
                    self.students.pop(index)
                    self.all_ID.discard(id)
                    break
        else:
            raise errors.InvalidDataError("Такого ID нету")
    def updateMark(self, student_data):
        if len(student_data) > 3:
            raise errors.InvalidDataError("Вы ввели слишком много данных")
        if len(student_data) < 3:
            raise errors.InvalidDataError("Вы ввели слишком мало данных")
        try:
            id = int(student_data[0].strip())
            mark_number = int(student_data[1].strip())
            mark = int(student_data[2].strip())
            if not id in self.all_ID:
                raise errors.InvalidDataError("Введённого ID не существует")
            if mark_number < 1 or mark_number > self.count_marks:
                raise errors.InvalidDataError("Введённый номер оценки не существует")
            if mark < 0 or mark > 100:
                raise errors.InvalidDataError("Введённая оценка некорректна")
            for el in self.students:
                if el.id == id:
                    el.changeMark(mark_number, mark)
                    break
        except ValueError:
            raise errors.InvalidDataError("Данные введены некорректно")
    def delMark(self, student_data):
        if len(student_data) > 2:
            raise errors.InvalidDataError("Вы ввели слишком много данных")
        if len(student_data) < 2:
            raise errors.InvalidDataError("Вы ввели слишком мало данных")
        try:
            id = int(student_data[0].strip())
            mark_number = int(student_data[1].strip())
            if not id in self.all_ID:
                raise errors.InvalidDataError("Введённого ID не существует")
            if mark_number < 1 or mark_number > self.count_marks:
                raise errors.InvalidDataError("Введённый номер оценки не существует")
            for el in self.students:
                if el.id == id:
                    el.delMark(mark_number)
                    break
        except ValueError:
            raise errors.InvalidDataError("Данные введены некорректно")
    def sortID(self):
        self.students.sort(key=lambda student: student.getID())
    def sortName(self):
        self.students.sort(key=lambda student: student.getName())
    def sortAVG(self):
        self.students.sort(key=lambda student: student.getAverage(), reverse=True)
    def getTopN(self, n):
        try:
            count = int(n)
            if count < 1:
                raise errors.InvalidDataError("Введённое число N неположительное")
            if count > len(self.students):
                raise errors.InvalidDataError("Введённое число N превосходит количество студентов в кэше")
            return self.students[:count]
        except ValueError:
            raise errors.InvalidDataError("Введённое число N имеет неправильный формат")
    def output(self):
        return self.__printTopN(len(self.students))
    def outputTopN(self, count):
        return self.__printTopN(count)
    def __printTopN(self, count):
        all_line = ""
        for i in range(count):
            line = ""
            index = 0
            for line_el in self.students[i].output():
                if index == 0:
                    line += line_el
                else:
                    line += ", " + line_el
                index += 1
            all_line += line
            all_line += '\n'
        return all_line
    def is_empty(self):
        if len(self.students) == 0:
            return True
        return False
    def clear(self):
        self.students.clear()
        self.all_ID.clear()
