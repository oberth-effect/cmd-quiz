import src.cmd_quiz as q
import os
import sys

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(__file__)

if __name__ == '__main__':
    q.run_cli_app(application_path)
