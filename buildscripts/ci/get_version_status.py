import json
import os
import re
import sys
import urllib.request

LCPP_REPO = "ggml-org/llama.cpp"
VERSION_FILE = "src/lcpp_lib/__version__.py"
BASE_VERSION = "0.0.0"


def get_current_version():
    if not os.path.exists(VERSION_FILE):
        return None
    with open(VERSION_FILE, "r") as f:
        content = f.read()
        match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
        return match.group(1) if match else None


def get_repo_latest_tag(repo: str):
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    print(f"Fetching latest release info from {repo}...")
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        return data["tag_name"]


def get_lcpp_latest_tag():
    return get_repo_latest_tag(LCPP_REPO)


def main():
    current_ver = get_current_version()
    latest_tag = get_lcpp_latest_tag()

    if not latest_tag:
        print("Error: Could not determine latest upstream tag.")
        sys.exit(1)

    target_ver = f"{BASE_VERSION}{latest_tag}"

    github_output = os.environ.get("GITHUB_OUTPUT")

    print(f"Current local version: {current_ver}")
    print(f"Latest upstream tag: {latest_tag}")
    print(f"Target version: {target_ver}")

    updated = "true" if current_ver != target_ver else "false"

    if github_output:
        with open(github_output, "a") as f:
            f.write(f"updated={updated}\n")
            f.write(f"version={target_ver}\n")
            f.write(f"tag={latest_tag}\n")

    print(f"Updated: {updated}")


if __name__ == "__main__":
    main()
