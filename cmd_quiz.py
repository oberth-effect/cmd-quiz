import src.cmd_quiz as q
import pathlib

ROOT_PATH = pathlib.Path(__file__).parent

if __name__ == '__main__':
    q.run_cli_app(ROOT_PATH)
