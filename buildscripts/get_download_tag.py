import argparse
import json
import os
import sys
import urllib.request

REPO = "ggml-org/llama.cpp"
DOWNLOAD_DIR = "downloads"
VERSION_FILE = os.path.join(DOWNLOAD_DIR, "ver.txt")


def get_latest_tag():
    url = f"https://api.github.com/repos/{REPO}/releases/latest"
    print(f"Fetching latest release info from {REPO}...", file=sys.stderr)
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        return data["tag_name"]


def main():
    parser = argparse.ArgumentParser(description="Fetch latest llama.cpp version tag")
    parser.add_argument(
        "--save", action="store_true", help=f"Save tag to {VERSION_FILE}"
    )
    parser.add_argument("--tag", help="Build tag (e.g. b7903)")
    args = parser.parse_args()

    tag = args.tag or get_latest_tag()

    if args.save:
        print(f"Tag: {tag}", file=sys.stderr)
        if not os.path.exists(DOWNLOAD_DIR):
            os.makedirs(DOWNLOAD_DIR)
        with open(VERSION_FILE, "w") as f:
            f.write(tag)
        print(f"Saved to {VERSION_FILE}", file=sys.stderr)
    else:
        print(f"{tag}")


if __name__ == "__main__":
    main()
