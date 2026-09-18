from translate import (
    repo,
    merge_branch,
    get_file_changed,
    create_new_branch,
    translate_branch,
    translate_files,
    create_pull_request,
)

import translate
from dotenv import load_dotenv

import os
from openai import OpenAI

import argparse

load_dotenv()
parser = argparse.ArgumentParser()

parser.add_argument("--local", action="store_true")

parser.add_argument("--provider-url", type=str, default=None)

parser.add_argument("--api-key", type=str, help="ONLY IN LOCAL", default=None)

parser.add_argument("--ai-model", type=str)

args = parser.parse_args()

translate.AI_MODEL = args.ai_model

if not args.api_key:
    PROVIDER_API_KEY = os.environ.get("PROVIDER_API_KEY")
else:
    PROVIDER_API_KEY = args.api_key

translate.client = OpenAI(base_url=args.provider_url, api_key=PROVIDER_API_KEY)

print(args.provider_url)


def main():
    repo.checkout(translate_branch)

    new_branch = create_new_branch()

    repo.checkout(new_branch)

    file_changed = get_file_changed(new_branch)

    merge_branch(new_branch)

    translate_files(file_list=file_changed, new_branch=new_branch)

    if not args.local and os.environ.get("GITHUB_TOKEN"):
        create_pull_request(new_branch)


if __name__ == "__main__":
    main()
