import argparse
import os

VERSION_FILE = "src/lcpp_lib/__version__.py"
VER_TXT = "downloads/ver.txt"
NIGHTLY_TXT = "downloads/nightly-tag.txt"
BASE_VERSION = "0.0.0"


def read_file(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read().strip()
    return None


def parse_semver(tag):
    """Extract the semver from a tag like 'v1.0.0'. Returns '0.0.0' if missing."""
    if tag:
        return tag.lstrip("v")
    return BASE_VERSION


def main():
    parser = argparse.ArgumentParser(description="Update lcpp_lib version file")
    parser.add_argument("--tag", help="Nightly tag (e.g. b7903)")
    parser.add_argument("--ver", help="Semver (e.g. 1.0.0)")
    args = parser.parse_args()

    version = parse_semver(args.ver or read_file(VER_TXT))
    nightly = args.tag or read_file(NIGHTLY_TXT) or ""

    new_version = f"{version}{nightly}"
    print(f"Writing {VERSION_FILE} with version: {new_version}")

    os.makedirs(os.path.dirname(VERSION_FILE), exist_ok=True)
    with open(VERSION_FILE, "w") as f:
        f.write(f'__version__ = "{new_version}"\n')


if __name__ == "__main__":
    main()
