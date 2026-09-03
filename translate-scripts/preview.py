from github import Github, Auth
import os
from pygit2 import Repository, Branch
from pygit2.enums import DeltaStatus, DiffOption, DiffFind
from pathlib import Path
from dataclasses import dataclass

from translate import (
    get_file_changed,
    get_content_blob_main,
    main_branch,
    translate_branch,
    translate_branch_name,
    main_branch_name,
    check_diff,
    get_github_repo,
)

if not check_diff():
    print("No change between main and translate branch")
    exit()


@dataclass
class FileChanged:
    type_of_changed: DeltaStatus
    path: Path


repo = Repository(".")


body = "Files to be translated: \n"

diff_github_link = f"https://github.com/writedev/book/compare/{translate_branch_name}...writedev:book:{main_branch_name}"

i = 1

for file in get_file_changed(translate_branch):  # for the numbered list
    if file.type_of_changed.name == "DELETED":
        file_link = (
            f"https://github.com/writedev/book/blob/{translate_branch_name}/{file.path}"
        )

        body += f"{i}. [{file.path}]({file_link}) is **{file.type_of_changed.name}**.\n"

        continue

    if file.type_of_changed.name == "RENAMED":
        continue

    file_link = f"https://github.com/writedev/book/blob/{main_branch_name}/{file.path}"

    number_of_carac = len(get_content_blob_main(file.path))

    i += 1

    body += f"{i}. [{file.path}]({file_link}) is **{file.type_of_changed.name}**. This file have `{number_of_carac}` of caractere.\n"


body += f"\nSee the diffs on **[github]({diff_github_link})**."

grepo = get_github_repo()

grepo.create_issue("Preview for translate main branch.", body=body)
