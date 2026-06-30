import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import time
load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

instruct = """You are a translator into French. You must remain objective and, above all, must not alter the content (the meaning) of the sentences you are translating. You must not add your own opinion. You must take the context of the translation into account. If you receive a code file, you must translate only what the user will see. You must NOT touch the technical aspects. YOU MUST ONLY RETURN THE ANSWER – NOTHING MORE THAN WHAT YOU ARE ASKED FOR. You therefore translate the raw text you receive."""


def is_okay(filename: str):
    file_path = Path(filename)
    response = input(f"Do you wants continue for {file_path.name} (Enter/n)")
    if "n" in response:
        return False
    return True

count = 0
total_time = 0

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
