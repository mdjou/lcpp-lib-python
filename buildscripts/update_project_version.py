import argparse
import os

VERSION_FILE = "src/lcpp_lib/__version__.py"
VER_TXT = "downloads/ver.txt"
BASE_VERSION = "0.0.0"


def get_tag_from_file():
    if os.path.exists(VER_TXT):
        with open(VER_TXT, "r") as f:
            return f.read().strip()
    return None


def main():
    parser = argparse.ArgumentParser(description="Update lcpp_lib version file")
    parser.add_argument("--tag", help="Build tag (e.g. b7903)")
    args = parser.parse_args()

    tag = args.tag or get_tag_from_file()
    if not tag:
        print(f"Error: Tag not specified and {VER_TXT} not found.")
        exit(1)

    new_version = f"{BASE_VERSION}{tag}"
    print(f"Writing {VERSION_FILE} with version: {new_version}")

    os.makedirs(os.path.dirname(VERSION_FILE), exist_ok=True)
    with open(VERSION_FILE, "w") as f:
        f.write(f'__version__ = "{new_version}"\n')


if __name__ == "__main__":
    main()
