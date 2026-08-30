from pygit2 import Repository, Commit, Branch
from pygit2.enums import (
    DeltaStatus,
)
from dataclasses import dataclass
import random
from pathlib import Path
from dotenv import load_dotenv
import os
from openai import OpenAI
import shutil


@dataclass
class FileChanged:
    type_of_changed: DeltaStatus
    path: Path


repo = Repository(".")

main_branch = repo.branches["test-main"]

translate_branch = repo.branches["test-translate-branch"]  # origin/translate-branch

load_dotenv()

client = OpenAI(base_url="http://localhost:11434/v1/", api_key="ollama")

INSTRUCT = open("translate-scripts/prompt.md").read()


def create_new_branch() -> Branch:
    """Create new random branch with the prefix "github-actions/" """

    repo.checkout(translate_branch)

    new_branch = repo.create_branch(
        f"github-actions/{random.randrange(0, 1000)}", translate_branch.peel(Commit)
    )

    return new_branch


def get_file_changed(new_branch: Branch) -> list[FileChanged]:
    """Retrun a list of file changed between the branch in params and the main branch"""

    repo.checkout(translate_branch)

    docs_file_changed: list[FileChanged] = []
    for diff in repo.diff(new_branch, main_branch):
        file = diff.delta.new_file
        path = Path(file.path)

        # Display the diff with the path
        print(f"{diff.delta.status.name} - {path}")

        if str(path).startswith("src/") and "img/" in str(path):
            docs_file_changed.append(
                FileChanged(type_of_changed=diff.delta.status, path=path)
            )

    return docs_file_changed


def merge_branch(new_branch: Branch) -> None:
    """Merge the main branch in the branch in the params."""
    repo.checkout(new_branch)

    # Merge the branch
    repo.merge(main_branch)

    # Get the head of both branch
    our_head = repo.head.target
    their_head = repo.head.target
    # Get the signature
    user = repo.default_signature
    # Write the tree in the index
    tree = repo.index.write_tree()
    # Write the message
    message = "Merging branches"
    # Send the message
    repo.create_commit("HEAD", user, user, message, tree, [their_head, our_head])

    repo.state_cleanup()


def get_content_blob(path: Path) -> str:
    """Get the content of a blob in string with its path"""
    tree = repo.head.peel(Commit).tree

    blob = tree / str(path)

    return blob.data.decode()


def get_content_blob_main(path: Path) -> str:
    """Get the content of a blob (in the main branch) in string with its path"""

    tree = main_branch.peel(Commit).tree

    blob = tree / str(path)

    content = blob.data.decode()

    return content


def do_update_commit(message: str = "Initial commit"):
    """Index all modification and create a commit."""

    ref = repo.head.name
    parents = [repo.head.target]

    index = repo.index

    index.add_all()
    index.write()
    author = repo.default_signature
    committer = repo.default_signature
    message = "Initial commit"
    tree = index.write_tree()
    repo.create_commit(ref, author, committer, message, tree, parents)


def translate_files(file_list: list[FileChanged], new_branch: Branch) -> None:

    # Delete all IMG folder and copy the new

    shutil.rmtree("translate-src/img")

    shutil.copytree("src/img", "translate-src/img")

    for files in file_list:
        if files.type_of_changed.name == "DELETED":
            # Delete file in src if is DELETED in the src

            delete_file = f"translate-src/{files.path.name}"

            if os.path.exists(delete_file):
                os.remove(delete_file)

            print(f"Files {delete_file} deleted")

            do_update_commit()

        elif (
            files.type_of_changed.name == "MODIFIED"
            or files.type_of_changed.name == "ADDED"
        ):
            # Traduct the content and create or modified a file.

            content = get_content_blob_main(files.path)

            new_file = f"translate-src/{files.path.name}"

            # Call IA api for traduct the document

            print("IA Call...")
            response = client.responses.create(
                model="qwen2.5-coder:7b", instructions=INSTRUCT, input=content
            )

            print("---output---\n")
            print(response.output_text)

            # Write the file
            open(new_file, mode="w+").write(response.output_text)

            print(f"{files.path} translated in {new_file}.")

            do_update_commit()
        else:
            print(
                f"---THIS TYPE OF CHANGE iSNT WORK || {files.type_of_changed.name}||---"
            )


def main():
    repo.checkout(translate_branch)

    new_branch = create_new_branch()

    file_changed = get_file_changed(new_branch)

    merge_branch(new_branch)

    translate_files(file_list=file_changed, new_branch=new_branch)


if __name__ == "__main__":
    main()

# def main() -> None:
#     new_branch = create_new_branch()

#     repo.checkout(new_branch)
