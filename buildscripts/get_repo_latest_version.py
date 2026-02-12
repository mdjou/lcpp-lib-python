import argparse
import json
import os
import urllib.request

REPO = "ggml-org/llama.cpp"
DOWNLOAD_DIR = "downloads"
VERSION_FILE = os.path.join(DOWNLOAD_DIR, "ver.txt")


def get_latest_tag():
    url = f"https://api.github.com/repos/{REPO}/releases/latest"
    print(f"Fetching latest release info from {REPO}...")
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        return data["tag_name"]


def main():
    parser = argparse.ArgumentParser(description="Fetch latest llama.cpp version tag")
    parser.add_argument(
        "--save", action="store_true", help=f"Save tag to {VERSION_FILE}"
    )
    args = parser.parse_args()

    tag = get_latest_tag()
    print(f"Latest tag: {tag}")

    if args.save:
        if not os.path.exists(DOWNLOAD_DIR):
            os.makedirs(DOWNLOAD_DIR)
        with open(VERSION_FILE, "w") as f:
            f.write(tag)
        print(f"Saved to {VERSION_FILE}")


if __name__ == "__main__":
    main()
