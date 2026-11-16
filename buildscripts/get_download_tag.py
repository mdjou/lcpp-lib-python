import argparse
import json
import os
import sys
import urllib.request

REPO = "ggml-org/llama.cpp"
DOWNLOAD_DIR = "downloads"
VERSION_FILE = os.path.join(DOWNLOAD_DIR, "ver.txt")
NIGHTLY_FILE = os.path.join(DOWNLOAD_DIR, "nightly-tag.txt")
NIGHTLY_ASSET_NAME = "nightly-tag.txt"


def fetch_json(url):
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read().decode())


def fetch_text(url):
    with urllib.request.urlopen(url) as response:
        return response.read().decode().strip()


def get_release_latest():
    url = f"https://api.github.com/repos/{REPO}/releases/latest"
    print(f"Fetching latest release info from {REPO}...", file=sys.stderr)
    return fetch_json(url)


def get_release_by_tag(tag):
    url = f"https://api.github.com/repos/{REPO}/releases/tags/{tag}"
    print(f"Fetching release info for tag {tag}...", file=sys.stderr)
    return fetch_json(url)


def get_nightly_tag_from_release(release):
    """Read the nightly tag from the release's nightly-tag.txt asset."""
    for asset in release.get("assets", []):
        if asset["name"] == NIGHTLY_ASSET_NAME:
            return fetch_text(asset["browser_download_url"])
    raise ValueError(
        f"Asset {NIGHTLY_ASSET_NAME} not found in release {release.get('tag_name')}"
    )


def get_latest_release_tags():
    """Return (version_tag, nightly_tag) for the latest release."""
    release = get_release_latest()
    version_tag = release["tag_name"]
    nightly_tag = get_nightly_tag_from_release(release)
    return version_tag, nightly_tag


def main():
    parser = argparse.ArgumentParser(description="Fetch latest llama.cpp version tag")
    parser.add_argument(
        "--save", action="store_true", help=f"Save tags to {DOWNLOAD_DIR}"
    )
    parser.add_argument(
        "--tag",
        help="Build tag (e.g. b7903) or release tag (e.g. v1.0.0)",
    )
    args = parser.parse_args()

    if args.tag:
        if args.tag.startswith("v"):
            # A release with the same structure as "latest":
            # track both the semver tag and its nightly tag.
            release = get_release_by_tag(args.tag)
            version_tag = release["tag_name"]
            nightly_tag = get_nightly_tag_from_release(release)
        else:
            # A nightly tag: only track the nightly version.
            version_tag = None
            nightly_tag = args.tag
    else:
        version_tag, nightly_tag = get_latest_release_tags()

    if args.save:
        if not os.path.exists(DOWNLOAD_DIR):
            os.makedirs(DOWNLOAD_DIR)
        if version_tag is not None:
            with open(VERSION_FILE, "w") as f:
                f.write(version_tag)
            print(f"Saved version to {VERSION_FILE}", file=sys.stderr)
        with open(NIGHTLY_FILE, "w") as f:
            f.write(nightly_tag)
        print(f"Saved nightly tag to {NIGHTLY_FILE}", file=sys.stderr)
    else:
        if version_tag is not None:
            print(f"{version_tag}-{nightly_tag}")
        else:
            print(nightly_tag)


if __name__ == "__main__":
    main()
