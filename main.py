import csv
import logging
import argparse

# Настройка логгера
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NameDescriptor:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not value.isalpha() or not value.istitle():
            print(f"{self.name} должно состоять только из букв и начинаться с заглавной буквы")
        else:
            instance.__dict__[self.name] = value


class Student:
    name = NameDescriptor()

    def __init__(self, name, subjects_file):
        self.__dict__['name'] = name
        self.__dict__['subjects'] = {}  # Присваиваем напрямую, чтобы избежать вызова __setattr__
        self.load_subjects(subjects_file)

    def load_subjects(self, subjects_file):
        try:
            with open(subjects_file, 'r', encoding='utf-8') as file:
                subjects_list = file.readline().strip().split(',')
                self.subjects = {subject: {'grades': [], 'test_scores': []} for subject in subjects_list}
        except FileNotFoundError:
            logging.error(f"Файл {subjects_file} не найден")
        except UnicodeDecodeError:
            logging.error(
                f"Ошибка декодирования файла {subjects_file}. Пожалуйста, убедитесь, что файл использует корректную кодировку.")

    def __setattr__(self, name, value):
        if name in self.subjects:
            if not isinstance(value, (int, float)):
                logging.warning(f"Оценка должна быть целым числом от 2 до 5")
            elif 2 <= value <= 5:
                self.subjects[name]['grades'].append(value)
            else:
                logging.warning(f"Оценка должна быть целым числом от 2 до 5")
        else:
            self.__dict__[name] = value

    def __getattr__(self, name):
        if name == 'subjects':
            return self.__dict__[name]  # Просто возвращаем значение из словаря
        elif name in self.subjects:
            return self.subjects[name]
        else:
            logging.warning(f"Предмет {name} не найден")

    def add_grade(self, subject, grade):
        setattr(self, subject, grade)

    def add_test_score(self, subject, test_score):
        if subject in self.subjects:
            if not isinstance(test_score, (int, float)):
                logging.warning(f"Результат теста должен быть целым числом от 0 до 100")
            elif 0 <= test_score <= 100:
                self.subjects[subject]['test_scores'].append(test_score)
            else:
                logging.warning(f"Результат теста должен быть целым числом от 0 до 100")
        else:
            logging.warning(f"Предмет {subject} не найден")

    def get_average_test_score(self, subject):
        if subject in self.subjects and self.subjects[subject]['test_scores']:
            return sum(self.subjects[subject]['test_scores']) / len(self.subjects[subject]['test_scores'])
        else:
            logging.warning(f"Нет данных о тестах по предмету {subject}")

    def get_average_grade(self):
        all_grades = [grade for subject in self.subjects.values() for grade in subject['grades']]
        if all_grades:
            return sum(all_grades) / len(all_grades)
        else:
            logging.warning("Нет данных о оценках")

    def __str__(self):
        subjects_list = ", ".join(self.subjects.keys())
        return f"Студент: {self.name}\nПредметы: {subjects_list}"

def main():
    parser = argparse.ArgumentParser(description='Обработка данных студента.')
    parser.add_argument('subjects_file', type=str, help='Путь к файлу с предметами и их результатами')
    args = parser.parse_args()

    student = Student("Иван Иванов", args.subjects_file)
    print(student)

if __name__ == "__main__":
    main()
