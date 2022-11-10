"""Graphical interface for the app"""
import tkinter as tk

from test_logic import Quizzer


class App:
    title = "MS_DOS Test App"

    window: tk.Tk
    quiz: Quizzer

    gui_progress: tk.Label
    progress: tk.StringVar
    gui_points: tk.Label
    points: tk.StringVar
    gui_attempts: tk.Label
    attempts: tk.StringVar

    gui_question_text: tk.Message
    question_text: tk.StringVar

    gui_prompt_text: tk.Label
    prompt_text: tk.StringVar

    gui_answer_box: tk.Entry
    gui_confirm_button: tk.Button

    def __init__(self, q: Quizzer):
        self.quiz = q

        # Initialise GUI
        self.window = tk.Tk()
        self.window.title(self.title)
        # Display State
        self.progress = tk.StringVar(value='Loading')
        self.gui_progress = tk.Label(textvariable=self.progress)
        self.gui_progress.grid(row=0, column=0)
        self.attempts = tk.StringVar(value='Loading')
        self.gui_attempts = tk.Label(textvariable=self.attempts)
        self.gui_attempts.grid(row=0, column=1)
        self.points = tk.StringVar(value='Loading')
        self.gui_points = tk.Label(textvariable=self.points)
        self.gui_points.grid(row=0, column=2)
        # Display Question Text
        self.question_text = tk.StringVar(value='Loading')
        self.gui_question_text = tk.Message(textvariable=self.question_text)
        self.gui_question_text.grid(row=1, column=1)
        # Display Prompt Text
        self.prompt_text = tk.StringVar(value='Loading')
        self.gui_prompt_text = tk.Label(textvariable=self.prompt_text)
        self.gui_prompt_text.grid(row=2, column=0)
        # Display Answer Box
        self.gui_answer_box = tk.Entry()
        self.gui_answer_box.grid(row=2, column=1)
        self.gui_confirm_button = tk.Button(text="OK")
        self.gui_confirm_button.grid(row=2, column=3)

        self._render_data()

    def _render_data(self):
        q, pts = self.quiz.state
        self.progress.set(f"otázka: {self.quiz.question_number}/{self.quiz.to_ask}")
        self.attempts.set(f"Zbývá pokusů: {q.att_rem}")
        self.points.set(f"body: {pts} b.")

        self.question_text.set(q.question_text)
        self.prompt_text.set(q.cmd_prompt)

    def _handle_attempt(self):
        pass

    def run(self):
        self.window.mainloop()
