""" The datamodel and evaluation logic of questions

Answer - single answer and check for it
Question - question information, attempts made, and checks for all possible answers
QuestionGroup - question group list, which question was selected
Quizzer - quiz logic
"""
import random


class Answer:
    """Abstraction of an answer

    properties:
    answer_text - text of the answer
    case_sensitive - Yes/No check case of answer

    methods:
    check_answer - checks given string against answer
    """
    answer_text: str
    case_sensitive: bool

    def __init__(self, answer_text: str, case_sensitive=False):
        """Intilise the Answer object

        parameters:
        answer_text - text of the answer
        cs_sen (optional) - control whether the answer is CaSe SeNSItIVE, default=False
        """
        self.answer_text = str(answer_text)
        self.case_sensitive = bool(case_sensitive)

    def check_answer(self, s: str) -> bool:
        """Check match for given answer"""
        # Remove unnecessary whitespaces
        " ".join(s.split())
        if self.case_sensitive:
            return s == self.answer_text
        else:
            return s.lower() == self.answer_text.lower()


class Question:
    """Abstraction of a question

    properties:
    gui_question_text - Text of the question
    cmd_prompt - the prompt displayed for the question
    correct_answers - list[Answer] of correct answers. len must be > 0
    attempts_permitted - number of permitted attempts, default=2
    scoring - points awarded for attempt in order of tries. If len(scoring) < attempts_permitted,
              the last value is used for each subsequent attempt, default=[2,1]
    attempts_remaining - remaining attempts for the question

    methods:
    attempt - validates an answer attempt
    """
    # Parameters
    question_text: str
    cmd_prompt: str
    correct_answers: list[Answer]
    attempts_permitted: int
    scoring: list[int]

    # Runtime variables
    asked: bool
    attempts_made: int
    attempted_answers: list[tuple[str, bool]]
    points_awarded: int | None

    def __init__(self, question_text: str,
                 prompt: str,
                 answers: list[Answer | str | tuple[str, bool]],
                 attempts=2,
                 scoring=(2, 1)):
        """Initialise the Question object

        parameters:
        question_text - Text of the question
        prompt - The path line of the 'cmd'
        answers - list of correct answers either as a  list[Answer] or as list[str] or list[tuple[str,bool]. Must have at least one element.
        attempts (optional) - number of attempts permitted, default=2
        scoring (optional) - scoring for attempts in order, default=[2,1]
        """
        # Handle parameters
        self.question_text = str(question_text)
        self.cmd_prompt = str(prompt)
        self.correct_answers = []
        if not len(answers) > 0:
            raise RuntimeError(f"Question '{self.question_text}' is missing a valid answer")
        for a in answers:
            if isinstance(a, Answer):
                self.correct_answers.append(a)
            if isinstance(a, str):
                self.correct_answers.append(Answer(a))
            if isinstance(a, tuple):
                self.correct_answers.append(Answer(a[0], a[1]))

        if not int(attempts) > 0:
            raise RuntimeError(f"Question '{self.question_text}' must have at least one attempt permitted")
        self.attempts_permitted = int(attempts)
        self.scoring = [*scoring, *[scoring[-1] * (self.attempts_permitted - len(scoring))]]

        # Initialise runtime vars
        self.asked = False
        self.attempts_made = 0
        self.attempted_answers = []
        self.points_awarded = None

    def attempt(self, attempt: str) -> tuple[bool, int]:
        """Validate an answer attempt. Return True/False and points awarded"""
        if self.attempts_remaining > 0:
            self.attempts_made += 1
            check = self._check_answers(attempt)
            self.attempted_answers.append((attempt, check))
            points = self.scoring[self.attempts_made - 1] if check else 0
            self.points_awarded = points
            return check, points
        else:
            return False, 0

    @property
    def attempts_remaining(self) -> int:
        """Remaining attempts"""
        return self.attempts_permitted - self.attempts_made

    def _check_answers(self, s: str) -> bool:
        """Checks for all possible answers"""
        for ans in self.correct_answers:
            if ans.check_answer(s):
                return True
        return False


class QuestionGroup:
    """Abstraction of a question group"""

    questions: list[Question]
    selected_question: Question

    def __init__(self, questions: list[Question]):
        self.questions = questions

    def get_random_question(self) -> Question:
        """Return random question from the group - does not check for repeats"""
        r = random.randrange(0, len(self.questions))
        q = self.questions[r]
        self.selected_question = q
        return q


class Quizzer:
    """Handle the quiz flow
    Will ask one question from each question group

    properties:
    question - Question currently being asked
    pts - Points already gained
    progress - current progress status
    curr_q_num - current question number
    ended - whether last attempt at last question was made
    asked_questions - all asked questions

    methods:
    attempt_answer - validate an answer attempt and change state
    """
    # Parameters

    # Runtime vars
    _new_groups: list[QuestionGroup]
    _asked_group: list[QuestionGroup]
    _current_question: Question
    _points_gained: int
    _ended: bool

    def __init__(self, groups: list[QuestionGroup]):
        """Initialise Quizzer object

        parameters:
        questions - list of possible questions
        """
        # Handle parameters
        # Initialise runtime vars
        self._new_groups = groups
        self._asked_group = []
        self._points_gained = 0
        self._ended = False

        # Get first question
        self._get_new_question()

    def attempt_answer(self, attempt: str) -> bool:
        """Check answer attempt, if correct return True, if incorrect return False.
        State changes:
        answer correct: load new question, award points
        answer incorrect: if 0 remaining attempts load new question
        """
        check, pts = self._current_question.attempt(attempt)
        if check:
            self._points_gained += pts
            self._get_new_question()
            return True
        else:
            if self._current_question.attempts_remaining <= 0:
                self._get_new_question()
            return False

    @property
    def question(self) -> Question:
        """Getter for current question"""
        return self._current_question

    @property
    def pts(self) -> int:
        """Getter for points gained"""
        return self._points_gained

    @property
    def ended(self) -> bool:
        """Getter for quiz end"""
        return self._ended

    @property
    def curr_q_num(self) -> int:
        """Return the current question (group) number"""
        return len(self._asked_group)

    @property
    def progress(self) -> tuple[int, int]:
        """Return progress status (x out of y questions)"""
        return self.curr_q_num, len(self._groups)

    @property
    def asked_questions(self) -> list[Question]:
        """Return all questions (not groups!) alerady asked"""
        return [g.selected_question for g in self._asked_group]

    def _get_new_question(self):
        """Load new question and change the state accordingly"""
        if len(self._new_groups) > 0:
            # Get random index
            ind = self._generate_random_group_index()
            # Remove from new_questions list and add to asked_questions
            group = self._new_groups.pop(ind)
            self._asked_group.append(group)
            question = group.get_random_question()
            # set internal state
            question.asked = True
            # set as current question
            self._current_question = question
        else:
            self._ended = True

    def _generate_random_group_index(self) -> int:
        """Generate new unique random group index"""
        return random.randrange(0, len(self._new_groups))

    @property
    def _groups(self) -> list[QuestionGroup]:
        """Return all groups"""
        return self._new_groups + self._asked_group
