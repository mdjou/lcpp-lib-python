import argparse
import json
import os
import urllib.request

REPO = "ggml-org/llama.cpp"
DOWNLOAD_DIR = "downloads"
VERSION_FILE = os.path.join(DOWNLOAD_DIR, "ver.txt")


def get_release_by_tag(tag):
    url = f"https://api.github.com/repos/{REPO}/releases/tags/{tag}"
    print(f"Fetching release info for tag {tag}...")
    try:
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching release: {e}")
        return None


def download_file(url, dest):
    print(f"Downloading {url} to {dest}...")
    urllib.request.urlretrieve(url, dest)


def get_saved_version():
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "r") as f:
            return f.read().strip()
    return None


def main():
    parser = argparse.ArgumentParser(description="Download llama.cpp vulkan release")
    parser.add_argument(
        "--version",
        help="Version tag (e.g. b7903). If not provided, reads from downloads/ver.txt",
    )
    args = parser.parse_args()

    version = args.version or get_saved_version()
    if not version:
        print(
            f"Error: Version not specified and {VERSION_FILE} not found. Run fetch_latest_version.py first."
        )
        exit(1)

    release = get_release_by_tag(version)
    if not release:
        print(f"Could not find release for tag: {version}")
        exit(1)

    assets = release["assets"]
    target_asset = None
    for asset in assets:
        name = asset["name"]
        if (
            "ubuntu" in name.lower()
            and "vulkan" in name.lower()
            and "x64" in name.lower()
            and name.endswith(".tar.gz")
        ):
            target_asset = asset
            break

    if target_asset:
        if not os.path.exists(DOWNLOAD_DIR):
            os.makedirs(DOWNLOAD_DIR)

        download_url = target_asset["browser_download_url"]
        filename = target_asset["name"]
        dest_path = os.path.join(DOWNLOAD_DIR, filename)

        download_file(download_url, dest_path)
        print(f"Successfully downloaded {filename}")
    else:
        print(
            f"Could not find a matching Ubuntu Vulkan release asset for version {version}."
        )
        exit(1)


if __name__ == "__main__":
    main()
