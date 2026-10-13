from lab.errors import InvalidDataError

class Student:
    def __init__(self, student_id, name, grades):
        self.marks_count = 0
        self.id = self._check_id(student_id)
        self.name = self._check_name(name)
        self.grades = self._check_grades(grades)
    def _check_id(self, val):
        try:
            int_val = int(val)
            if int_val <= 0:
                raise ValueError()
            return int_val
        except ValueError:
            raise InvalidDataError("ID должен быть положительным целым числом")
    def _check_name(self, val):
        if not val.strip():
            raise InvalidDataError("ФИО студента не может быть пустым.")
        return val.strip()
    def _check_grades(self, val):
        if not isinstance(val, list):
            raise InvalidDataError("Оценки должны быть списком.")
        try:
            nums = []
            for el in val:
                if el.strip() == "":
                    nums.append(-100)
                else:
                    num = int(el.strip())
                    if num != -100:
                        if num < 0 or num > 100:
                            raise ValueError
                    nums.append(num)
                    self.marks_count += 1
            return nums
        except (ValueError):
            raise InvalidDataError("Оценки должны быть целыми числами от 0 до 100 или отсутствовать.")
    def output(self):
        return self.__my_output()
    def output_with_AVG(self):
        output_list = self.__my_output()
        output_list.append(str(self.getAverage()))
        return output_list
    def __my_output(self):
        output_list = []
        output_list.append(str(self.id))
        output_list.append(self.name)
        for el in self.grades:
            if el != -100:
                output_list.append(str(el))
            else:
                output_list.append(" ")
        return output_list
    def changeMark(self, mark_number, mark):
        if self.grades[mark_number - 1] == -100:
            self.marks_count += 1
        self.grades[mark_number - 1] = mark
    def delMark(self, mark_number):
        self.grades[mark_number - 1] = -100
        self.marks_count -= 1
    def getAverage(self):
        sum = 0
        count = 0
        for el in self.grades:
            if el != -100:
                sum += el
                count += 1
        if count == 0:
            return 0
        return sum / count
    def getMarksCount(self):
        return self.marks_count
    def getID(self):
        return self.id
    def getName(self):
        return self.name
