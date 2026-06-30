import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import time

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

instruct = """You are a translator into French. You must remain objective and, above all, must not alter the content (the meaning) of the sentences you are translating. You must not add your own opinion. You must take the context of the translation into account. If you receive a code file, you must translate only what the user will see. You must NOT touch the technical aspects. YOU MUST ONLY RETURN THE ANSWER – NOTHING MORE THAN WHAT YOU ARE ASKED FOR. You therefore translate the raw text you receive."""


def translate_all():

    count = 0

    for filename in os.listdir(os.getcwd() + "/src"):
        # print(filename)

        start_duration = time.time()

        if ".md" not in filename:
            continue

        path = os.path.join(os.getcwd() + "/src", filename)

        with open(path, "r+") as f:
            print("traduction...")

            response = client.responses.create(
                model="gpt-4o-mini", instructions=instruct, input=f.read()
            )

            # with open(path, mode="w"):
            #     pass

            f.seek(0)
            f.truncate()

            f.write(response.output_text)

            count += 1
            duration = time.time() - start_duration

            print(f"{count}-{filename}-- a été traduit en {duration}!")


def translate_a_file(file: str, not_translate_texte :str):
    if ".md" not in file:
        return

    path = Path(os.path.join(os.getcwd() + "/src", file))

    if not path.is_file():
        return print("Ce n'est pas un fichier")

    with open(path, mode="r+") as f:
        print(f"traduction... du fichier {file}")

        response = client.responses.create(
            model="gpt-4o-mini", instructions=instruct, input=not_translate_texte
        )

        f.seek(0)
        f.truncate()

        f.write(response.output_text)

    print("Fichier traduit avec succes")

NOT_TRANSLATE="""
# The Rust Programming Language

_by Steve Klabnik, Carol Nichols, and Chris Krycho, with contributions from the
Rust Community_

This version of the text assumes you’re using Rust 1.96.0 (released 2026-05-28)
or later with `edition = "2024"` in the *Cargo.toml* file of all projects to
configure them to use Rust 2024 Edition idioms. See the [“Installation” section
of Chapter 1][install]<!-- ignore --> for instructions on installing or
updating Rust, and see [Appendix E][appendix-e]<!-- ignore --> for information
on editions.

The HTML format is available online at
[https://doc.rust-lang.org/stable/book/](https://doc.rust-lang.org/stable/book/)
and offline with installations of Rust made with `rustup`; run `rustup doc
--book` to open.

Several community [translations] are also available.

This text is available in [paperback and ebook format from No Starch
Press][nsprust].

[install]: ch01-01-installation.html
[appendix-e]: appendix-05-editions.html
[nsprust]: https://nostarch.com/rust-programming-language-3rd-edition
[translations]: appendix-06-translation.html

> **🚨 Want a more interactive learning experience? Try out a different version
> of the Rust Book, featuring: quizzes, highlighting, visualizations, and
> more**: <https://rust-book.cs.brown.edu>
"""

if __name__ == "__main__":
    translate_a_file("title-page.md", NOT_TRANSLATE)
