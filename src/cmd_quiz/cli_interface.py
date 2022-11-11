""" CLI interface implementation for the quiz app

App - run the quiz
Error - display error messages
"""

import time
import os

from .quiz_logic import Quizzer


class _GUIElements:
    @staticmethod
    def _clear():
        """Clears the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def _print_banner():
        """Prints the top banner"""
        print(r"###################################################")
        print(r"#    __  __  _____        _____   ____   _____    #")
        print(r"#   |  \/  |/ ____|      |  __ \ / __ \ / ____|   #")
        print(r"#   | \  / | (___ _______| |  | | |  | | (___     #")
        print(r"#   | |\/| |\___ \_______| |  | | |  | |\___ \    #")
        print(r"#   | |  | |____) |      | |__| | |__| |____) |   #")
        print(r"#   |_|  |_|_____/       |_____/ \____/|_____/    #")
        print(r"#              _____ ___ ___ _____                #")
        print(r"#             |_   _| __/ __|_   _|               #")
        print(r"#               | | | _|\__ \ | |                 #")
        print(r"#               |_| |___|___/ |_|                 #")
        print(r"###################################################")

    @staticmethod
    def _print_line():
        """Prints a line"""
        print("---------------------------------------------------")

    @staticmethod
    def _print_line_short():
        print("-------")


class App(_GUIElements):
    quiz = Quizzer

    def __init__(self, q: Quizzer):
        self.quiz = q

    def run(self):
        """The main program loop"""
        # Question loop
        while not self.quiz.ended:
            self._clear()
            self._print_banner()
            self._print_state()
            self._ask_question()
        # Results
        self._clear()
        self._print_banner()
        self._print_results()

    @staticmethod
    def end():
        """Final loop"""
        while input("Napište 'exit' pro konec: ") != 'exit':
            pass

    def _print_state(self):
        """Prints the current state variables"""
        q = self.quiz.question
        pts = self.quiz.pts
        p1, p2 = self.quiz.progress
        self._print_line()
        print(f"| Otázka: {p1 / p2}     Zbývající pokusy: {q.attempts_remaining}     Body: {pts} |")
        self._print_line()

    def _ask_question(self):
        """Prints the question and validates the answer"""
        q = self.quiz.question
        print(f"Otázka {self.quiz.curr_q_num}:")
        print(q.question_text)
        self._print_line()
        # Wait for nonempty input
        while not len((answer := input(f"{q.cmd_prompt} "))) > 0:
            pass
        result = self.quiz.attempt_answer(answer)
        print("Správně" if result else "Špatně")
        time.sleep(1)

    def _print_results(self):
        """Prints the final results of the quiz"""
        max_points = 0
        for i, q in enumerate(self.quiz.asked_questions):
            print(f"Otázka {i + 1}:{q.question_text}")
            self._print_line_short()
            print("Zadané odpovědi:")
            for a in q.attempted_answers:
                print(f"  {'Správně' if a[1] else 'Špatně '}   {a[0]}")
            self._print_line_short()
            print(f"Zisk bodů {q.points_awarded}/{max(q.scoring)}")
            max_points += max(q.scoring)
            self._print_line()

        print(f"CELKEM BODŮ: {self.quiz.pts}/{max_points}")
        self._print_line()


class Error(_GUIElements):
    """Exception printout"""

    def __init__(self, e: Exception | str):
        print("Při běhu programu se vyskytla tato chyba:")
        self._print_line_short()
        print(e)
        self._print_line()
