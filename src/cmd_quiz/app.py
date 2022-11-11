import pathlib
import yaml

from .cli_interface import App, Error
from .quiz_logic import Quizzer, Question, QuestionGroup

QUESTION_FILE_LOOKUP_LOCATIONS = [
    'questions',
    'data/questions',
]

SUPPORTED_FORMATS = ['yml', 'yaml']


def _parse_question_file_yaml(pth: pathlib.Path) -> list[QuestionGroup]:
    """Parser for yaml question file"""
    with open(pth, 'r') as f:
        raw_data = yaml.safe_load(f)
        return [QuestionGroup([Question(q['text'], q['prompt'], q['answers']) for q in qs]) for g, qs in
                raw_data.items()]


def _get_loc_list(root_pth: pathlib.Path):
    return [root_pth / loc for loc in QUESTION_FILE_LOOKUP_LOCATIONS]


def _find_question_file(root_pth: pathlib.Path) -> pathlib.Path:
    att_loc = []
    for p in _get_loc_list(root_pth):
        for fmt in SUPPORTED_FORMATS:
            pth = p.parent / f"{p.name}.{fmt}"
            att_loc.append(pth)
            if pth.is_file():
                return pth
    loc_print = '\n'.join(map(str, att_loc))
    raise RuntimeError(f"No datafile found. Searched:\n{loc_print}")


def run_cli_app(root_path: pathlib.Path | str):
    try:
        qf = _find_question_file(pathlib.Path(root_path))
        quiz = Quizzer(_parse_question_file_yaml(qf))
        app = App(quiz)
        app.run()
    except Exception as e:
        Error(e)
    finally:
        App.end()
