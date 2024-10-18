import os
import tqdm
import regex
import requests

from pydantic import BaseModel


def search_for_py_files(directory):
    paths = []
    for root, _, files in tqdm.tqdm(os.walk(directory), desc="Processing files"):
        for file in files:
            if file.endswith('.py'):
                paths.append(os.path.join(root, file))
    return paths


def build_issue_from_todo_lines(todo_lines):
    issues = []
    description_pattern = regex.compile(r".*Desctiption:.*")
    for i, code in todo_lines.items():
        title = code.split("#")[1].split("TODO:")[1].strip()
        body = code.split("#")[1].strip()
        issues.append(Issue(title=title, body=body))
    return issues


def extract_todo_lines(code):
    todo_pattern = regex.compile(r".*#.*TODO:.*")
    additional_line_pattern = regex.compile(r".*#.*")

    todo_lines = {}
    for i, line in enumerate(code):
        if todo_pattern.match(line):
            todo_lines[i] = line

    for i, code in todo_lines.items():
        if additional_line_pattern.match(code[i + 1]):
            todo_lines[i] += code[i + 1].repalce("#", "")

    return todo_lines


def create_github_issue(repo, title, body, labels):
    url = f"https://api.github.com/repos/{repo}/issues"
    token = os.getenv('GITHUB_TOKEN')
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    issue = {
        "title": title,
        "body": body,
        "labels": labels
    }
    response = requests.post(url, json=issue, headers=headers)
    if response.status_code == 201:
        print("Successfully created issue.")
    else:
        print(f"Failed to create issue: {response.status_code}")
        print(response.json())


class Issue(BaseModel):
    title: str
    body: str


def todo_to_issue(root_directory):
    paths = search_for_py_files(root_directory)
    issues = []
    for path in paths:
        with open(path, 'r') as file:
            code = file.readlines()

        todo_lines = extract_todo_lines(code)
        issues = build_issue_from_todo_lines(
            todo_lines,
            os.basename(path)
        )
