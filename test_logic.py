""" The datamodel and evaluation logic of questions
"""
import random


class Answer:
    """Abstraction of an answer

    attributes:
    answer_text - text of the answer
    """
    answer_text: str
    case_sensitive: bool

    def __init__(self, a_text: str, cs_sen=False):
        """Intilise the Answer object

        parameters:
        a_text - text of the answer
        cs_sen (optional) - control whether the answer is CaSe SeNSItIVE, default=False
        """
        self.answer_text = str(a_text)
        self.case_sensitive = bool(cs_sen)

    def check_answer(self, att_ans: str) -> bool:
        """Check match for answer"""
        # Remove unnecessary whitespaces
        " ".join(att_ans.split())
        if self.case_sensitive:
            return att_ans == self.answer_text
        else:
            return att_ans.lower() == self.answer_text.lower()


class Question:
    """Abstraction of a question

    attributes:
    gui_question_text - Text of the question
    cmd_prompt - the prompt displayed for the question
    correct_answers - list[Answer] of correct answers. len must be > 0
    attempts_permitted - number of permitted attempts, default=2
    scoring - points awarded for attempt in order of tries. If len(scoring) < attempts_permitted,
              the last value is used for each subsequent attempt, default=[2,1]
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
    attempted_answers: list[str]
    points_awarded: int | None

    def __init__(self, q_text: str, prompt: str, answers: list[Answer | str | tuple[str, bool]], attempts=2,
                 scoring=(2, 1)):
        """Initialise the Question object

        parameters:
        q_text - Text of the question
        answers - list of correct answers either as a  list[Answer] or as list[string]. Must have at least one element.
        attempts (optional) - number of attempts permitted, default=2
        scoring (optional) - scoring for attempts in order, default=[2,1]
        """
        # Handle parameters
        self.question_text = str(q_text)
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
        if self.att_rem > 0:
            self.attempts_made += 1
            self.attempted_answers.append(attempt)
            check = self._check_answers(attempt)
            points = self.scoring[self.attempts_made - 1] if check else 0
            return check, points
        else:
            return False, 0

    @property
    def att_rem(self) -> int:
        """Remaining attempts"""
        return self.attempts_permitted - self.attempts_made

    def _check_answers(self, att_answer: str) -> bool:
        """Checks for all possible answers"""

        for ans in self.correct_answers:
            if ans.check_answer(att_answer):
                return True
        return False


class Quizzer:
    """Handle the quiz flow"""
    # Parameters
    to_ask: int
    show_correct: bool

    # Runtime vars
    new_questions: list[Question]
    asked_questions: list[Question]
    current_question: Question
    points_gained: int
    ended: bool

    def __init__(self, questions: list[Question], q_number=10, show_corr=False):
        """Initialise Quizzer object"""
        # Handle parameters
        self.to_ask = int(q_number)
        self.show_correct = bool(show_corr)
        # Initialise runtime vars
        self.new_questions = questions
        self.asked_questions = []
        if len(self.new_questions) < self.to_ask:
            raise RuntimeError("Not enough questions loaded")
        self.points_gained = 0
        self.ended = False

        # Get first question
        self._get_new_question()

    def attempt_answer(self, attempt: str) -> bool:
        """Check answer attempt, if correct return True, if incorrect return False.
        State changes:
        answer correct: load new question, award points
        answer incorrect: if 0 remaining attempts load new question
        """
        check, pts = self.current_question.attempt(attempt)
        if check:
            self.points_gained += pts
            self._get_new_question()
            return True
        else:
            if self.current_question.att_rem <= 0:
                self._get_new_question()
            return False

    def _get_new_question(self):
        """Load new question and change the state accordingly"""
        # Check for quiz end
        if self.question_number == self.to_ask:
            self.ended = True
            return
        # Get random index
        ind = self._generate_random_question_index()
        # Remove from new_questions list and add to asked_questions
        question = self.new_questions.pop(ind)
        self.asked_questions.append(question)
        # set internal state
        question.asked = True
        # set as current question
        self.current_question = question

    def _generate_random_question_index(self) -> int:
        """Generate new unique random question from the list"""
        return random.randrange(0, len(self.new_questions))

    @property
    def state(self) -> tuple[Question, int]:
        """Current question and points"""
        return self.current_question, self.points_gained

    @property
    def questions(self) -> list[Question]:
        """All questions"""
        return self.new_questions + self.asked_questions

    @property
    def question_number(self) -> int:
        """Returns the current question number"""
        return len(self.asked_questions)
