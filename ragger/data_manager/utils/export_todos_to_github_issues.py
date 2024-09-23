""" TODOs to Github Issues
This is an internal tool which will be extracted to a separate repository
before publishing version 1.0.0. The tool searches for TODOs comments in
source code files and creates Github issues from them. The TODOs will be
structured with keywords such as "Description", "Task" and "Tags" to
provide necessary information needed for the issue. This will be executed
as part of the Github Actions where issues will be collected and matched
with already existing issues to avoid duplicates. Furthermore, the CI/CD
will not allow merging of code to the master branch if there are any
unresolved issues that concern the merged dev branch.

Example:
# TODO: Description: some task description. Task: Create a program
# for exporting in-code todos to github issues. Tags: feature, monitoring

"""

import os
import tqdm
import regex
import requests

from pydantic import BaseModel
from typing import List


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
    tags: List[str]


def todo_to_issue(root_directory):
    paths = search_for_py_files(root_directory)
    issues = []
    for path in paths:
        with open(path, 'r') as file:
            code = file.readlines()

        todo_lines = find_todos(code)
        extract_description


def find_todos(code):
    todo_pattern = regex.compile(r"^(.*TODO:).*#*\n.*")
    return todo_pattern.findall(code)


def extract_description(match):
    # following regex matches the description between "Description:"
    # and "Task:" or "Tags:"
    description_pattern = regex.compile(r".*Description:(.*)Task:.*")


def extract_task(match):
    pass