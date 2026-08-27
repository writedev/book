from pygit2 import Repository, Commit, Branch, Blob
from pygit2.enums import DeltaStatus
from dataclasses import dataclass
import random
from pathlib import Path
from dotenv import load_dotenv
import os
from openai import OpenAI


@dataclass
class FileChanged:
    type_of_changed: DeltaStatus
    path: Path


repo = Repository(".")

main_branch = repo.branches["test-main"]

translate_branch = repo.branches["test-translate-branch"]  # origin/translate-branch

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

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
    docs_file_changed: list[FileChanged] = []
    for diff in repo.diff(main_branch, new_branch):
        # file = diff.delta.new_file

        file = diff.delta.new_file
        path = Path(file.path)

        # if file.path.startswith("src/") and file.path.endswith(".md"):
        #     filename = file.path.split("/")[1]

        #     print(filename)

        # print(f"{diff.delta.status.name} - {path}")

        # print(path.name)

        if str(path).startswith("src/"):  # VERIFY IF THERE ARE NOT IN IMG
            tree = main_branch.peel(Commit).tree

            blob = tree / str(path)

            if isinstance(blob, Blob):
                docs_file_changed.append(
                    FileChanged(type_of_changed=diff.delta.status, path=path)
                )

    return docs_file_changed


def merge_branch(new_branch: Branch) -> None:
    """Merge the main branch in the branch in the params"""
    repo.checkout(new_branch)

    repo.merge(main_branch)


def get_content_blob(path: Path) -> str:
    """Get the content of a blob in string with its path"""
    tree = repo.head.peel(Commit).tree

    blob = tree / str(path)

    return blob.data.decode()


def translate_files(file_list: list[FileChanged]) -> None:

    repo.checkout(main_branch)

    for files in file_list:
        if files.type_of_changed.name == "DELETED":
            os.remove(files.path)
            print(f"{files.path} deleted.")

        elif (
            files.type_of_changed.name == "MODIFIED"
            or files.type_of_changed.name == "ADDED"
        ):
            content = get_content_blob(files.path)
            response = client.responses.create(
                model="gpt-4o-mini", instructions=INSTRUCT, input=content
            )

            new_file = f"translate-src/{files.path.name}"

            open(new_file, mode="w+").write(response.output_text)

            print(f"{files.path} translated in {new_file}.")

            # open(mode="+w")


# print(get_file_changed())

# check_if_diff()


def main():
    new_branch = create_new_branch()

    file_changed = get_file_changed(new_branch)

    merge_branch(new_branch)

    translate_files(file_changed)

    print()


if __name__ == "__main__":
    main()

# def main() -> None:
#     new_branch = create_new_branch()

#     repo.checkout(new_branch)
