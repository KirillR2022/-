import pytest
import tempfile
import os
from main import Student

@pytest.fixture
def student_instance():
    subjects_csv = tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8')
    subjects_csv.write("Математика,Физика,История,Литература\n")
    subjects_csv.close()

    student = Student("Иван Иванов", subjects_csv.name)

    yield student

    os.remove(subjects_csv.name)


def test_add_grade(student_instance):
    student_instance.add_grade("Математика", 4)
    assert student_instance.Математика['grades'] == [4]


def test_add_test_score(student_instance):
    student_instance.add_test_score("История", 75)
    assert student_instance.История['test_scores'] == [75]


def test_get_average_test_score(student_instance):
    student_instance.add_test_score("История", 75)
    student_instance.add_test_score("История", 85)
    assert student_instance.get_average_test_score("История") == 80


def test_get_average_grade(student_instance):
    student_instance.add_grade("Математика", 4)
    student_instance.add_grade("Физика", 5)
    assert student_instance.get_average_grade() == 4.5



