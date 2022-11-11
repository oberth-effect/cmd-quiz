import pathlib
import yaml

from cli_interface import App, Error
from test_logic import Quizzer, Question, QuestionGroup

ROOT_PATH = pathlib.Path(__file__).parent

QUESTION_FILE_LOOKUP_LOCATIONS = [
    ROOT_PATH / 'questions',
    ROOT_PATH / 'data/questions',
]

SUPPORTED_FORMATS = ['yml', 'yaml']


def parse_question_file_yaml(pth: pathlib.Path) -> list[QuestionGroup]:
    """Parser for yaml question file"""
    with open(pth, 'r') as f:
        raw_data = yaml.safe_load(f)
        return [QuestionGroup([Question(q['text'], q['prompt'], q['answers']) for q in qs]) for g, qs in
                raw_data.items()]


def find_question_file() -> pathlib.Path:
    for p in QUESTION_FILE_LOOKUP_LOCATIONS:
        for fmt in SUPPORTED_FORMATS:
            pth = p.parent / f"{p.name}.{fmt}"
            print(pth)
            if pth.is_file():
                return pth
    raise RuntimeError("No datafile found.")


if __name__ == "__main__":
    try:
        qf = find_question_file()
        quiz = Quizzer(parse_question_file_yaml(qf))
        app = App(quiz)
        app.run()
    except Exception as e:
        Error(e)
    finally:
        App.end()
