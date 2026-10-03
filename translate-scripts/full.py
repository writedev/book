from openai import OpenAI, AsyncOpenAI
from dotenv import load_dotenv
import time
import asyncio
import os
import argparse

load_dotenv()

# Parser Part
parser = argparse.ArgumentParser()

parser.add_argument("--provider-url", type=str, default=None)

parser.add_argument("--api-key", type=str, help="ONLY IN LOCAL", default=None)

parser.add_argument("--ai-model", type=str)

parser.add_argument("--sync", action="store_true")

args = parser.parse_args()

# Constant Part
if not args.api_key:
    PROVIDER_API_KEY = os.environ.get("PROVIDER_API_KEY")
else:
    PROVIDER_API_KEY = args.api_key

AI_MODEL = args.ai_model

PROVIDER_API_KEY = args.api_key

INSTRUCT = open("prompt.md").read()

client = AsyncOpenAI(base_url=args.provider_url, api_key=PROVIDER_API_KEY)


async def traduct_file(filename: str, new_path: str, count: str):
    """Translate a file and write it to the translate directory with asyncio"""

    print(f"Traduction of {filename}...")

    start_time = time.time()

    response = await client.responses.create(
        model=AI_MODEL,
        instructions=INSTRUCT,
        input=open(f"src/{filename}", mode="r").read(),  # Return the original file
    )

    open(new_path, "w+").write(response.output_text)

    print(
        f"{count} -- {filename}-- have been translated in {round(time.time() - start_time, 2)}!"
    )

    return filename


async def translate_all_async():
    """Traduct the all files in src/ directory"""
    count = 0

    total_duration = time.time()

    # get only the markdown files
    file_list = [x for x in os.listdir(os.getcwd() + "/src") if x.endswith(".md")]

    tasks = []

    for filename in file_list:
        count += 1

        # Create a readable counter in string
        count_format = f"{count}/{len(file_list)}"

        # Transform the path in for the translate directory
        new_path = os.path.join(os.getcwd() + "/translate-src", filename)

        if args.sync:
            await traduct_file(filename, new_path, count_format)
        else:
            tasks.append(traduct_file(filename, new_path, count_format))

    if not args.sync:
        # launch all functions in parrallel
        await asyncio.gather(*tasks)

    print(
        f"-- The translation of all the files took {round(time.time() - total_duration, 2)}s"
    )


if __name__ == "__main__":
    asyncio.run(translate_all_async())

    # translate_all()
