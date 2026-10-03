from openai import OpenAI, AsyncOpenAI
from dotenv import load_dotenv
import time
import asyncio
import os

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1", api_key=os.environ.get("PROVIDER_API_KEY")
)

async_client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1", api_key=os.environ.get("PROVIDER_API_KEY")
)

AI_MODEL = "openai/gpt-oss-120b"

# AI_MODEL = "deepseek/deepseek-v4.1-flash"


############################################
#                   SYNC                   #
############################################


def translate_all():
    """Traduct the all files in src/ directory."""

    count = 0

    total_duration = time.time()

    for filename in os.listdir(os.getcwd() + "/src"):
        # print(filename)

        start_time = time.time()

        if ".md" not in filename:
            continue

        path = os.path.join(os.getcwd() + "/translate-src", filename)

        print("Traduction...")

        response = client.responses.create(
            model=AI_MODEL,
            instructions=open("prompt.md", mode="r").read(),
            input=open(f"src/{filename}", mode="r").read(),  # openai/gpt-oss-120b
        )

        open(path, "w+").write(response.output_text)

        count += 1

        print(
            f"{count} -- {filename}-- have been translated in {round(time.time() - start_time, 2)}!"
        )

    print(
        f"-- The translation of all the files took {round(time.time() - total_duration, 2)}s"
    )


############################################
#                   ASYNC                   #
############################################


async def traduct_file(filename: str, path: str, count: str):
    """Translate a file and write it to the translate directory"""

    print(f"Traduction of {filename}...")

    start_time = time.time()

    response = await async_client.responses.create(
        model=AI_MODEL,
        instructions=open("prompt.md", mode="r").read(),
        input=open(f"src/{filename}", mode="r").read(),  # openai/gpt-oss-120b
    )

    open(path, "w+").write(response.output_text)

    print(
        f"{count} -- {filename}-- have been translated in {round(time.time() - start_time, 2)}!"
    )

    return filename


async def translate_all_async():
    """Traduct the all files in src/ directory with asyncio"""
    count = 0

    total_duration = time.time()

    # get only the markdown files
    file_list = [x for x in os.listdir(os.getcwd() + "/src") if x.endswith(".md")]

    tasks = []

    for filename in file_list:
        if not filename.endswith(".md"):
            continue

        # Transform the path in for the translate directory

        path = os.path.join(os.getcwd() + "/translate-src", filename)

        count += 1

        tasks.append(traduct_file(filename, path, f"{count}/{len(file_list)}"))

    await asyncio.gather(*tasks)

    print(
        f"-- The translation of all the files took {round(time.time() - total_duration, 2)}s"
    )


if __name__ == "__main__":
    asyncio.run(translate_all_async())

    # translate_all()
