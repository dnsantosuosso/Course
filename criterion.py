"""CSC148 Assignment 1

=== CSC148 Winter 2020 ===
Department of Computer Science,
University of Toronto

=== Module Description ===

This file contains classes that describe different types of criteria used to
evaluate a group of answers to a survey question.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from survey import Question, Answer

class InvalidAnswerError(Exception):
    """
    Error that should be raised when an answer is invalid for a given question.
    """


def invalid_answer(question: Question, answers: List[Answer]) -> None:
    """
    Raise InvalidAnswerError if any answer in <answers> is not a valid
    answer to <question>.
    """
    for answer in answers:
        if not question.validate_answer(answer):
            raise InvalidAnswerError


def only_one_valid(question: Question, answers: List[Answer]) -> bool:
    """
    Evaluate if there is only one answer in <answers> and it is valid.
    """
    return len(answers) == 1 and question.validate_answer(answers[0])


class Criterion:
    """
    An abstract class representing a criterion used to evaluate the quality of
    a group based on the group members' answers for a given question.
    """

    def score_answers(self, question: Question, answers: List[Answer]) -> float:
        """
        Return score between 0.0 and 1.0 indicating the quality of the group of
        <answers> to the question <question>.

        Raise InvalidAnswerError if any answer in <answers> is not a valid
        answer to <question>.

        Each implementation of this abstract class will measure quality
        differently.
        """
        raise NotImplementedError


class HomogeneousCriterion(Criterion):
    """
    A criterion used to evaluate the quality of a group based on the group
    members' answers for a given question.

    This criterion gives a higher score to answers that are more similar.
    """

    def score_answers(self, question: Question, answers: List[Answer]) -> float:
        """
        Return a score between 0.0 and 1.0 indicating how similar the answers in
        <answers> are.

        This score is calculated by finding the similarity of every
        combination of two answers in <answers> and taking the average of all
        of these similarity scores.

        If there is only one answer in <answers> and it is valid return 1.0
        since a single answer is always identical to itself.

        Raise InvalidAnswerError if any answer in <answers> is not a valid
        answer to <question>.

        === Precondition ===
        len(answers) > 0
        """
        invalid_answer(question, answers)
        if only_one_valid(question, answers):
            return 1.0
        sim_scores = 0
        num = 0
        for i in range(len(answers) - 1):
            for j in range(i + 1, len(answers)):
                sim_scores += question.get_similarity(answers[i], answers[j])
                num += 1
        return sim_scores / num


class HeterogeneousCriterion(Criterion):
    """ A criterion used to evaluate the quality of a group based on the group
    members' answers for a given question.

    This criterion gives a higher score to answers that are more different.
    """

    def score_answers(self, question: Question, answers: List[Answer]) -> float:
        """
        Return a score between 0.0 and 1.0 indicating how similar the answers in
        <answers> are.

        This score is calculated by finding the similarity of every
        combination of two answers in <answers>, finding the average of all
        of these similarity scores, and then subtracting this average from 1.0

        If there is only one answer in <answers> and it is valid, return 0.0
        since a single answer is never identical to itself.

        Raise InvalidAnswerError if any answer in <answers> is not a valid
        answer to <question>.

        === Precondition ===
        len(answers) > 0
        """
        invalid_answer(question, answers)
        if only_one_valid(question, answers):
            return 0.0
        sim_scores = 0
        num = 0
        for i in range(len(answers) - 1):
            for j in range(i + 1, len(answers)):
                sim_scores += question.get_similarity(answers[i], answers[j])
                num += 1
        return 1.0 - sim_scores / num


class LonelyMemberCriterion(Criterion):
    """ A criterion used to measure the quality of a group of students
    according to the group members' answers to a question. This criterion
    assumes that a group is of high quality if no member of the group gives
    a unique answer to a question.
    """

    def score_answers(self, question: Question, answers: List[Answer]) -> float:
        """
        Return score between 0.0 and 1.0 indicating the quality of the group of
        <answers> to the question <question>.

        The score returned will be zero iff there are any unique answers in
        <answers> and will be 1.0 otherwise.

        An answer is not unique if there is at least one other answer in
        <answers> with identical content.

        Raise InvalidAnswerError if any answer in <answers> is not a valid
        answer to <question>.

        === Precondition ===
        len(answers) > 0
        """
        # TODO: complete the body of this method
        for answer in answers:
            if answer.is_valid(question):
                num = 0
                while num != len(answers) - 1:
                    if answers[num].content != answers[num + 1].content:
                        return 0.0
                    num += 1
                return 1.0
            else:
                raise InvalidAnswerError


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={'extra-imports': ['typing',
                                                  'survey']})
