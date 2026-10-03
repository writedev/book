import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import time

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1", api_key=os.environ.get("PROVIDER_API_KEY")
)

instruct = """You are a translator into French. You must remain objective and, above all, must not alter the content (the meaning) of the sentences you are translating. You must not add your own opinion. You must take the context of the translation into account. If you receive a code file, you must translate only what the user will see. You must NOT touch the technical aspects. YOU MUST ONLY RETURN THE ANSWER – NOTHING MORE THAN WHAT YOU ARE ASKED FOR. You therefore translate the raw text you receive."""

AI_MODEL = "openai/gpt-oss-120b"


def translate_all():

    count = 0

    total_duration = 0

    for filename in os.listdir(os.getcwd() + "/src"):
        # print(filename)

        start_duration = time.time()

        if ".md" not in filename:
            continue

        path = os.path.join(os.getcwd() + "/src", filename)

        with open(path, "r+") as f:
            print("traduction...")

            response = client.responses.create(
                model=AI_MODEL,
                instructions=instruct,
                input=f.read(),  # openai/gpt-oss-120b
            )

            # with open(path, mode="w"):
            #     pass

            f.seek(0)
            f.truncate()

            f.write(response.output_text)

            count += 1
            duration = time.time() - start_duration

            total_duration += duration

            print(f"{count}-{filename}-- a été traduit en {round(duration, 2)}!")

    print(f"La traduction de tous les fichiers a prit {round(total_duration, 2)}s")


def translate_a_file(file: str):
    if ".md" not in file:
        return

    translate_path = Path(os.path.join(os.getcwd() + "/translate-src", file))

    base_path = Path(os.path.join(os.getcwd() + "/src", file))

    if not base_path.is_file() and not translate_path.is_file():
        return print("Ce n'est pas un fichier commun entre translate-scripts/ et src/")

    time_started = time.time()

    with open(translate_path, mode="w+") as f:
        print(f"traduction... du fichier {base_path}")

        response = client.responses.create(
            model=AI_MODEL,
            instructions=open("translate-scripts/prompt2.md", mode="r").read(),
            input=base_path.open().read(),
        )

        f.seek(0)
        f.truncate()

        f.write(response.output_text)

        print(f"fichier {base_path} traduit vers {translate_path}")

        print("-------------------------")

        print(base_path.open("r").read())

        print("-------------------------")

        print(response.output_text)

        print("-------------------------")

        print(f"Le temps de reponse est de {round(time.time() - time_started, 2)}")


def fake_translate_a_file(file: str):
    if not file.endswith(".md"):
        return

    translate_path = Path("translate-src", file)

    base_path = Path("src", file)

    if not base_path.is_file() and not translate_path.is_file():
        return print("Ce n'est pas un fichier commun entre translate-scripts/ et src/")

    print(f"traduction... du fichier {base_path}")

    time_started = time.time()

    response = client.responses.create(
        model="inception/mercury-2.5",
        instructions=open("translate-scripts/prompt2.md", mode="r").read(),
        input=base_path.open().read(),
    )

    print(f"fichier {base_path} traduit vers {translate_path}")

    print("-------------------------")

    print(base_path.open("r").read())

    print("-------------------------")

    print(response.output_text)

    print("-------------------------")

    print(f"Le temps de reponse est de {round(time.time() - time_started, 2)}")


if __name__ == "__main__":
    fake_translate_a_file("ch05-03-method-syntax.md")
