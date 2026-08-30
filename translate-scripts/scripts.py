from pygit2 import Repository, Commit, Branch, Blob, Signature
from pygit2.enums import (
    DeltaStatus,
    MergeFlag,
    MergeFileFlag,
    MergeFavor,
    MergeAnalysis,
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

INSTRUCT = """You are a translator into French. You must remain objective and, above all, must not alter the content (the meaning) of the sentences you are translating. You must not add your own opinion. You must take the context of the translation into account. If you receive a code file, you must translate only what the user will see. You must NOT touch the technical aspects. YOU MUST ONLY RETURN THE ANSWER – NOTHING MORE THAN WHAT YOU ARE ASKED FOR. You therefore translate the raw text you receive."""


def check_if_diff() -> bool:
    """check if there are diffs between the branchs"""
    diffs = []

    for diff in repo.diff(main_branch, translate_branch):
        # if "translate-src/" in diff.delta.new_file.path:
        #     continue

        if diff.delta.new_file.path.startswith("src"):
            print(diff.delta.new_file.path)

        diffs.append(diff)

    if diffs == []:
        return False
    return True


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
        # file = diff.delta.new_file
        file = diff.delta.new_file
        path = Path(file.path)

        # if file.path.startswith("src/") and file.path.endswith(".md"):
        #     filename = file.path.split("/")[1]

        #     print(filename)

        print(f"{diff.delta.status.name} - {path}")

        # print(path.name)

        if str(path).startswith("src/") and "img/" in str(
            path
        ):  # VERIFY IF THERE ARE NOT IN IMG
            tree = main_branch.peel(Commit).tree
            docs_file_changed.append(
                FileChanged(type_of_changed=diff.delta.status, path=path)
            )

    return docs_file_changed


def merge_branch(new_branch: Branch) -> None:
    """Merge the main branch in the branch in the params."""
    repo.checkout(new_branch)

    # analysis, preference = repo.merge_analysis(main_branch.target)

    repo.merge(main_branch)

    our_head = repo.head.target
    their_head = repo.head.target
    user = repo.default_signature
    tree = repo.index.write_tree()
    message = "Merging branches"
    new_commit = repo.create_commit(
        "HEAD", user, user, message, tree, [their_head, our_head]
    )

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
    author = Signature("Alice Author", "alice@authors.tld")
    committer = Signature("Cecil Committer", "cecil@committers.tld")
    message = "Initial commit"
    tree = index.write_tree()
    repo.create_commit(ref, author, committer, message, tree, parents)


def translate_files(file_list: list[FileChanged], new_branch: Branch) -> None:

    # repo.checkout(new_branch)

    # Delete all IMG folder and copy the new

    shutil.rmtree("translate-src/img")

    shutil.copytree("src/img", "translate-src/img")

    for files in file_list:
        if files.type_of_changed.name == "DELETED":
            delete_file = f"translate-src/{files.path.name}"

            if os.path.exists(delete_file):
                os.remove(delete_file)

            print(delete_file)

            do_update_commit()

        elif (
            files.type_of_changed.name == "MODIFIED"
            or files.type_of_changed.name == "ADDED"
        ):
            content = get_content_blob_main(files.path)
            print("---input---\n")
            # print(content)

            print("Openai Call...")
            response = client.responses.create(
                model="qwen2.5-coder:7b", instructions=INSTRUCT, input=content
            )
            # response = "hey"  # <- TEST

            new_file = f"translate-src/{files.path.name}"

            print("---output---\n")
            # print(response.output_text)

            open(new_file, mode="w+").write(response.output_text)

            print(f"{files.path} translated in {new_file}.")

            do_update_commit()
        else:
            print(
                f"---THIS TYPE OF CHANGE iSNT WORK || {files.type_of_changed.name}||---"
            )

        # open(mode="+w")


# print(get_file_changed())

# check_if_diff()


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
