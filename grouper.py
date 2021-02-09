"""CSC148 Assignment 1

=== CSC148 Winter 2020 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Misha Schwartz, Mario Badr, Christine Murad, Diane Horton, Sophia Huynh
and Jaisie Sin

All of the files in this directory and all subdirectories are:
Copyright (c) 2020 Misha Schwartz, Mario Badr, Christine Murad, Diane Horton,
Sophia Huynh and Jaisie Sin

=== Module Description ===

This file contains classes that define different algorithms for grouping
students according to chosen criteria and the group members' answers to survey
questions. This file also contain a classe that describes a group of students as
well as a grouping (a group of groups).
"""
from __future__ import annotations
import random
from typing import TYPE_CHECKING, List, Any
from course import sort_students
if TYPE_CHECKING:
    from survey import Survey
    from course import Course, Student


def slice_list(lst: List[Any], n: int) -> List[List[Any]]:
    """
    Return a list containing slices of <lst> in order. Each slice is a
    list of size <n> containing the next <n> elements in <lst>.

    The last slice may contain fewer than <n> elements in order to make sure
    that the returned list contains all elements in <lst>.

    === Precondition ===
    n <= len(lst)

    >>> slice_list([3, 4, 6, 2, 3], 2) == [[3, 4], [6, 2], [3]]
    True
    >>> slice_list(['a', 1, 6.0, False], 3) == [['a', 1, 6.0], [False]]
    True
    """
    # TODO: complete the body of this function
    final_list = []
    if n >= len(lst):
        final_list.append(lst)
        return final_list
    if n <= len(lst):
        count = 0
        sub_list = []
        for i in lst:
            if count != n:
                count = count + 1
                sub_list.append(i)
            else:
                count = 1
                final_list.append(sub_list)
                sub_list = [i]
        if len(sub_list) > 0:
            final_list.append(sub_list)
        return final_list
    return None


def windows(lst: List[Any], n: int) -> List[List[Any]]:
    """
    Return a list containing windows of <lst> in order. Each window is a list
    of size <n> containing the elements with index i through index i+<n> in the
    original list where i is the index of window in the returned list.

    === Precondition ===
    n <= len(lst)

    >>> windows([3, 4, 6, 2, 3], 2) == [[3, 4], [4, 6], [6, 2], [2, 3]]
    True
    >>> windows(['a', 1, 6.0, False], 3) == [['a', 1, 6.0], [1, 6.0, False]]
    True
    """
    final_list = []
    if n > len(lst):
        return final_list
    if n == len(lst):
        final_list.append(lst)
        return final_list
    if n <= len(lst):
        for i in range(len(lst)):
            if i + n <= len(lst):
                sub_list = []
                count = 0
                for j in range(len(lst)):
                    if count != n:
                        sub_list.append(lst[i + j])
                        count = count + 1
                    else:
                        final_list.append(sub_list)
                        break
            else:
                break
    return final_list


class Grouper:
    """
    An abstract class representing a grouper used to create a grouping of
    students according to their answers to a survey.

    === Public Attributes ===
    group_size: the ideal number of students that should be in each group

    === Representation Invariants ===
    group_size > 1
    """

    group_size: int

    def __init__(self, group_size: int) -> None:
        """
        Initialize a grouper that creates groups of size <group_size>

        === Precondition ===
        group_size > 1
        """
        # TODO: complete the body of this method
        self.group_size = group_size

    def make_grouping(self, course: Course, survey: Survey) -> Grouping:
        """ Return a grouping for all students in <course> using the questions
        in <survey> to create the grouping.
        """
        raise NotImplementedError


class AlphaGrouper(Grouper):
    """
    A grouper that groups students in a given course according to the
    alphabetical order of their names.

    === Public Attributes ===
    group_size: the ideal number of students that should be in each group

    === Representation Invariants ===
    group_size > 1
    """

    group_size: int

    def make_grouping(self, course: Course, survey: Survey) -> Grouping:
        """
        Return a grouping for all students in <course>.

        The first group should contain the students in <course> whose names come
        first when sorted alphabetically, the second group should contain the
        next students in that order, etc.

        All groups in this grouping should have exactly self.group_size members
        except for the last group which may have fewer than self.group_size
        members if that is required to make sure all students in <course> are
        members of a group.

        Hint: the sort_students function might be useful
        """
        # TODO: complete the body of this method
        m = Grouping()
        k = slice_list(sort_students(course.students, 'name'), self.group_size)
        for i in k:
            n = Group(i)
            m.add_group(n)
        return m


class RandomGrouper(Grouper):
    """
    A grouper used to create a grouping of students by randomly assigning them
    to groups.

    === Public Attributes ===
    group_size: the ideal number of students that should be in each group

    === Representation Invariants ===
    group_size > 1
    """

    group_size: int

    def make_grouping(self, course: Course, survey: Survey) -> Grouping:
        """
        Return a grouping for all students in <course>.

        Students should be assigned to groups randomly.

        All groups in this grouping should have exactly self.group_size members
        except for one group which may have fewer than self.group_size
        members if that is required to make sure all students in <course> are
        members of a group.
        """
        # TODO: complete the body of this method
        f_list = []
        m = course.students
        random.shuffle(m)
        for n in range(0, len(m), len(m)//(len(m)//self.group_size)):
            j = m[n:n+len(m)//(len(m)//self.group_size)]
            f_list.append(j)
        group_list = []
        for group in f_list:
            group_list.append(Group(group))
        grouping = Grouping()
        for group in group_list:
            grouping.add_group(group)
        return grouping



class GreedyGrouper(Grouper):
    """
    A grouper used to create a grouping of students according to their
    answers to a survey. This grouper uses a greedy algorithm to create
    groups.

    === Public Attributes ===
    group_size: the ideal number of students that should be in each group

    === Representation Invariants ===
    group_size > 1
    """

    group_size: int

    def make_grouping(self, course: Course, survey: Survey) -> Grouping:
        """
        Return a grouping for all students in <course>.

        Starting with a tuple of all students in <course> obtained by calling
        the <course>.get_students() method, create groups of students using the
        following algorithm:

        1. select the first student in the tuple that hasn't already been put
           into a group and put this student in a new group.
        2. select the student in the tuple that hasn't already been put into a
           group that, if added to the new group, would increase the group's
           score the most (or reduce it the least), add that student to the new
           group.
        3. repeat step 2 until there are N students in the new group where N is
           equal to self.group_size.
        4. repeat steps 1-3 until all students have been placed in a group.

        In step 2 above, use the <survey>.score_students method to determine
        the score of each group of students.

        The final group created may have fewer than N members if that is
        required to make sure all students in <course> are members of a group.
        """
        # TODO: complete the body of this method
        student_list = list(course.get_students())
        grouping = Grouping()
        group_size = self.group_size
        while len(student_list) >= group_size:
            group = Group([student_list[0]])
            del student_list[0]
            while group.__len__() < group_size:
                hscore = 0
                highest_index = 0
                for i in range(len(student_list)):
                    my_list = []
                    for student in group.get_members():
                        my_list.append(student)
                    temp_group = Group(my_list)
                    temp_group.add_member(student_list[i])
                    if survey.score_students(temp_group.get_members()) > hscore:
                        hscore = survey.score_students(temp_group.get_members())
                        highest_index = i
                group.add_member(student_list[highest_index])
                del student_list[highest_index]
            grouping.add_group(group)
        '''
        if len(student_list) != 0:
            group = Group(student_list)
            grouping.add_group(group)
        '''
        return grouping

class WindowGrouper(Grouper):
    """
    A grouper used to create a grouping of students according to their
    answers to a survey. This grouper uses a window search algorithm to create
    groups.

    === Public Attributes ===
    group_size: the ideal number of students that should be in each group

    === Representation Invariants ===
    group_size > 1
    """

    group_size: int

    def make_grouping(self, course: Course, survey: Survey) -> Grouping:
        """
        Return a grouping for all students in <course>.

        Starting with a tuple of all students in <course> obtained by calling
        the <course>.get_students() method, create groups of students using the
        following algorithm:

        1. Get the windows of the list of students who have not already been
           put in a group.
        2. For each window in order, calculate the current window's score as
           well as the score of the next window in the list. If the current
           window's score is greater than or equal to the next window's score,
           make a group out of the students in current window and start again at
           step 1. If the current window is the last window, compare it to the
           first window instead.

        In step 2 above, use the <survey>.score_students to determine the score
        of each window (list of students).

        In step 1 and 2 above, use the windows function to get the windows of
        the list of students.

        If there are any remaining students who have not been put in a group
        after repeating steps 1 and 2 above, put the remaining students into a
        new group.
        """
        grouping = Grouping()
        student_list = []
        for student in course.get_students():
            student_list.append(student)
        window_list = windows(student_list, self.group_size)
        while len(window_list) > 1:
            for i in range(len(window_list) - 1):
                current_score = survey.score_students(window_list[0])
                if i == len(window_list) - 1:
                    next_score = survey.score_students(window_list[0])
                else:
                    next_score = survey.score_students(window_list[i+1])
                if current_score >= next_score:
                    grouping.add_group(Group(window_list[i]))
                    del window_list[i]
        if len(window_list) != 0:
            grouping.add_group(Group(window_list[0]))
        # for i in range(len(window_list)):
        #     current_score = survey.score_students(window_list[i])
        #     if i == len(window_list) - 1:
        #         next_score = survey.score_students(window_list[0])
        #     else:
        #         next_score = survey.score_students(window_list[i+1])
        #     if current_score >= next_score:
        #         if len(window_list) > 1:
        #             grouping.add_group(Group(window_list[i]))
        #             del window_list[i]
        #         else:
        #             grouping.add_group(Group(window_list[0]))
        return grouping


class Group:
    """
    A group of one or more students

    === Private Attributes ===
    _members: a list of unique students in this group

    === Representation Invariants ===
    No two students in _members have the same id
    """

    _members: List[Student]

    def __init__(self, members: List[Student]) -> None:
        """ Initialize a group with members <members> """
        # TODO: complete the body of this method
        self._members = members

    def __len__(self) -> int:
        """ Return the number of members in this group """
        # TODO: complete the body of this method
        return len(self._members)

    def __contains__(self, member: Student) -> bool:
        """
        Return True iff this group contains a member with the same id
        as <member>.
        """
        # TODO: complete the body of this method
        for group_member in self._members:
            if group_member.id == member.id:
                return True
        return False

    def __str__(self) -> str:
        """
        Return a string containing the names of all members in this group
        on a single line.

        You can choose the precise format of this string.
        """
        # TODO: complete the body of this method
        member_names = ''
        for member in self._members:
            if member != self._members[-1]:
                member_names += member.name + ', '
            else:
                member_names += member.name + '.'
        return member_names

    def get_members(self) -> List[Student]:
        """ Return a list of members in this group. This list should be a
        shallow copy of the self._members attribute.
        """
        # TODO: complete the body of this method
        member_list = []
        for member in self._members:
            member_list.append(member)
        return member_list

    def add_member(self, member: Student) -> None:
        """
        Adds a student into the group.
        """
        # TODO: complete the body of this method
        self._members.append(member)


class Grouping:
    """
    A collection of groups

    === Private Attributes ===
    _groups: a list of Groups

    === Representation Invariants ===
    No group in _groups contains zero members
    No student appears in more than one group in _groups
    """

    _groups: List[Group]

    def __init__(self) -> None:
        """ Initialize a Grouping that contains zero groups """
        # TODO: complete the body of this method
        self._groups = []

    def __len__(self) -> int:
        """ Return the number of groups in this grouping """
        # TODO: complete the body of this method
        return len(self._groups)

    def __str__(self) -> str:
        """
        Return a multi-line string that includes the names of all of the members
        of all of the groups in <self>. Each line should contain the names
        of members for a single group.

        You can choose the precise format of this string.
        """
        # TODO: complete the body of this method
        group_members = ''
        for group in self._groups:
            group_members += group.__str__() + '\n'
        return group_members

    def add_group(self, group: Group) -> bool:
        """
        Add <group> to this grouping and return True.

        Iff adding <group> to this grouping would violate a representation
        invariant don't add it and return False instead.
        """
        # TODO: complete the body of this method
        if len(group.get_members()) == 0:
            return False
        for member in group.get_members():
            for grouped_group in self._groups:
                if member in grouped_group:
                    return False
        self._groups.append(group)
        return True

    def get_groups(self) -> List[Group]:
        """ Return a list of all groups in this grouping.
        This list should be a shallow copy of the self._groups
        attribute.
        """
        # TODO: complete the body of this method
        group_list = []
        for group in self._groups:
            group_list.append(group)
        return group_list


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={'extra-imports': ['typing',
                                                  'random',
                                                  'survey',
                                                  'course']})
