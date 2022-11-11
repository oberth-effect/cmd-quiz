# A Simple CMD quizzing tool

Build the executable:
```console
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --onefile --icon=cmd.ico cmd_quiz.py
```

Run the app without building executable:
```console
pip install -r requirements.txt
python cmd_quiz.py
```

## Configuration structure
By default, the program looks for these files (only one is necessary):

- `./questions.[yaml/yml]`
- `./data/questions.[yaml/yml]`

### YAML
```yaml
THIS IS A GROUP:
  - text: Question 1
    prompt: this\is\a\prompt>
    answers:
      - answer1
  - text: Question 2 
    prompt: another_prompt>
    answers:
      - answer 1
      - answer 2
      - answer 3
THIS IS ANOTHER GROUP:
  - text: Question 3
    prompt: yet_another_prompt>
    answers:
      - answer 1
      - answer 2
```