from github import Github, Auth, UnknownObjectException
from github.Label import Label
import os
from pygit2 import Repository, Branch
from pygit2.enums import DeltaStatus, DiffOption, DiffFind
from pathlib import Path
from dataclasses import dataclass

from translate_with_git import (
    get_file_changed,
    get_content_blob_main,
    LABEL_NAME,
    translate_branch,
    translate_branch_name,
    main_branch_name,
    check_diff,
    get_github_repo,
)

from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument(
    "--title-issue", type=str, default="build: update the translation of the docs"
)

args = parser.parse_args()

if not check_diff():
    print("No change between main and translate branch")
    exit()

#### SHOW THE NUMBER OF DIFFERENTE CARACTERE


@dataclass
class FileChanged:
    type_of_changed: DeltaStatus
    path: Path


repo = Repository(".")

repo.checkout(translate_branch)

grepo = get_github_repo()


def check_labels() -> Label:
    try:
        return grepo.get_label(LABEL_NAME)
    except UnknownObjectException:
        return grepo.create_label(LABEL_NAME, color="FFA500")


def get_issue_body() -> str:
    """Create the body in string for the new issue"""

    body = "Files to be translated: \n"

    i = 1

    for file in get_file_changed(translate_branch):  # for the numbered list
        # For see the file that is about to be deleted
        if file.type_of_changed.name == "DELETED":
            file_link = f"https://github.com/writedev/book/blob/{translate_branch_name}/{file.path}"

            body += (
                f"{i}. [{file.path}]({file_link}) is **{file.type_of_changed.name}**.\n"
            )

            continue

        if file.type_of_changed.name == "RENAMED":
            continue

        file_link = (
            f"https://github.com/writedev/book/blob/{main_branch_name}/{file.path}"
        )

        number_of_carac = len(get_content_blob_main(file.path))

        diff_of_carac = len(get_content_blob_main(file.path)) - len(
            open(file.path).read()
        )

        i += 1

        body += f"{i}. [{file.path}]({file_link}) is **{file.type_of_changed.name}**. This file has `{number_of_carac}` characters and **{'+' + str(diff_of_carac) if diff_of_carac > 0 else str(diff_of_carac)}** different characters. \n"

    diff_github_link = f"https://github.com/writedev/book/compare/{translate_branch_name}...writedev:book:{main_branch_name}"

    body += f"\nSee the diffs on **[github]({diff_github_link})**."

    return body


if __name__ == "__main__":
    grepo.create_issue(
        args.title_issue,
        body=get_issue_body(),
        labels=[check_labels()],
    )
