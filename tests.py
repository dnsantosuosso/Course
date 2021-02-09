"""CSC148 Assignment 1

=== CSC148 Winter 2020 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains sample tests for Assignment 1.
"""
from assignments.a1.a1.course import Student, Course
from assignments.a1.a1.survey import Question, Answer

#CLASS STUDENTS

def test__init__() -> None:
    student = Student(1, 'Jack')
    assert student.id == 1
    assert student.name == 'Jack'
    assert student.answers == {}


def test__str__() -> None:
    m = Student(5, 'Diego')
    assert m.__str__() == 'Diego'


def test_has_answer() -> None:
    m = Student(5, 'Diego')
    q = Question(5, 'Question Text')
    a = Answer(True)
    m.set_answer(q, a)
    assert m.has_answer(q) == True


def test_set_answer() -> None:
    m = Student(5, 'Diego')
    q = Question(5, 'Question Text')
    a = Answer(True)
    m.set_answer(q, a)
    assert m.has_answer(q) == True


def test_get_answer() -> None:
    m = Student(5, 'Diego')
    q1 = Question(5, 'Question Text 1')
    a = Answer(True)
    m.set_answer(q1, a)
    q2 = Question(6, 'Question Text 2')
    assert m.get_answer(q2) == None

#CLASS COURSE

def test_enroll_students() -> None:
    m = Student(5, 'Diego')
    c = Course('Math')
    c.enroll_students(m)
    assert c.get_students == m




if __name__ == '__main__':
    import pytest
    pytest.main(['tests.py'])
