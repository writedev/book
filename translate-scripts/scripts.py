from pygit2 import (
    Repository,
    Commit,
    Branch,
    RemoteCallbacks,
    Username,
    CredentialType,
    UserPass,
    Keypair,
)
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
from github import Auth, Github
import subprocess
import time

load_dotenv()


@dataclass
class FileChanged:
    type_of_changed: DeltaStatus
    path: Path


repo = Repository(".")

auth = Auth.Token(os.environ.get("GITHUB_TOKEN"))

g = Github(auth=auth)


main_branch = repo.branches["origin/test-main"]

translate_branch = repo.branches[
    "origin/test-translate-branch"
]  # origin/translate-branch

load_dotenv()

# client = OpenAI(base_url="http://localhost:11434/v1/", api_key="ollama")

INSTRUCT = open("translate-scripts/prompt.md").read()


def create_new_branch() -> Branch:
    """Create new random branch with the prefix "github-actions/" """

    # repo.checkout(translate_branch)

    new_branch = repo.create_branch(
        f"github-actions/{random.randrange(0, 1000)}", translate_branch.peel(Commit)
    )

    print("The branch is create ! ")

    return new_branch


def get_file_changed(new_branch: Branch) -> list[FileChanged]:
    """Retrun a list of file changed between the branch in params and the main branch"""

    docs_file_changed: list[FileChanged] = []
    for diff in repo.diff(new_branch, main_branch):
        file = diff.delta.new_file
        path = Path(file.path)

        # Display the diff with the path
        # print(f"{diff.delta.status.name} - {path}")

        if str(path).startswith("src/") and "img/" not in str(path):
            docs_file_changed.append(
                FileChanged(type_of_changed=diff.delta.status, path=path)
            )

            print(f"{diff.delta.status.name} - {path}")

    return docs_file_changed


def merge_branch(new_branch: Branch) -> None:
    """Merge the main branch in the branch in the params."""

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

    print("The merge is done !")

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

    print("The commit is done !")


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

            output_text = "hey"

            print("IA Call...")
            # response = client.responses.create(
            #     model="qwen2.5-coder:7b", instructions=INSTRUCT, input=content
            # )

            print("---output---\n")
            print(output_text)

            # Write the file
            open(new_file, mode="w+").write(output_text)

            print(f"{files.path} translated in {new_file}.")

            do_update_commit()
        else:
            print(
                f"---THIS TYPE OF CHANGE iSNT WORK || {files.type_of_changed.name}||---"
            )


def create_pull_request(new_branch: Branch):

    cmd = subprocess.run(
        f"git push origin {new_branch.branch_name}", capture_output=True, shell=True
    )

    print(cmd.stdout)

    print("Git push is done !")

    time.sleep(3)

    grepo = g.get_repo(os.environ.get("GITHUB_REPOSITORY"))

    pull_request = grepo.create_pull(
        base=translate_branch.branch_name,
        head=new_branch.branch_name,
        title="My Test Pull Request",
        body="This pull request is a test!",
    )

    print("The pull request is done !")


def main():
    repo.checkout(translate_branch)

    new_branch = create_new_branch()

    repo.checkout(new_branch)

    file_changed = get_file_changed(new_branch)

    merge_branch(new_branch)

    translate_files(file_list=file_changed, new_branch=new_branch)

    create_pull_request(new_branch)


if __name__ == "__main__":
    main()

# def main() -> None:
#     new_branch = create_new_branch()

#     repo.checkout(new_branch)
