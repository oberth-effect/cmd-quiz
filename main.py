import pathlib
import yaml

from graphical_interface import App
from test_logic import Quizzer, Question


def parse_question_file(pth: pathlib.Path) -> list[Question]:
    """Parser for question file. Currently does not support number of attempts, scoring, and case sensitivity"""
    with open(pth, 'r') as f:
        raw_data = yaml.safe_load(f)
        return [Question(qtxt, args['prompt'], args['answers']) for qtxt, args in raw_data.items()]


if __name__ == "__main__":
    q = Quizzer(parse_question_file('test.yaml'),3)
    app = App(q)
    app.run()
