import time

from test_logic import Quizzer


class App:
    quiz = Quizzer

    def __init__(self, q):
        self.quiz = q

    def run(self):
        while not self.quiz.ended:
            self._clear()
            self._print_banner()
            self._print_state()
            self._print_question()

    def _print_state(self):
        q, pts = self.quiz.state
        self._print_line()
        print(
            f"| Otázka: {self.quiz.question_number}/{self.quiz.to_ask}     Zbývající pokusy: {q.att_rem}     Body: {pts} |")
        self._print_line()

    def _print_question(self):
        q, _ = self.quiz.state
        print(f"Otázka {self.quiz.question_number}:")
        print(q.question_text)
        self._print_line()
        answer = input(q.cmd_prompt)
        result = self.quiz.attempt_answer(answer)
        message = "Správně" if result else "Špatně"
        print(message)
        time.sleep(1)

    @staticmethod
    def _clear():
        print("\033[H\033[J", end="")

    @staticmethod
    def _print_banner():
        print("###################################################")
        print("#    __  __  _____        _____   ____   _____    #")
        print("#   |  \/  |/ ____|      |  __ \ / __ \ / ____|   #")
        print("#   | \  / | (___ _______| |  | | |  | | (___     #")
        print("#   | |\/| |\___ \_______| |  | | |  | |\___ \    #")
        print("#   | |  | |____) |      | |__| | |__| |____) |   #")
        print("#   |_|  |_|_____/       |_____/ \____/|_____/    #")
        print("#               _____ ___ ___ _____               #")
        print("#              |_   _| __/ __|_   _|              #")
        print("#                | | | _|\__ \ | |                #")
        print("#                |_| |___|___/ |_|                #")
        print("###################################################")

    @staticmethod
    def _print_line():
        print("---------------------------------------------------")
