import os
import re
import sys

VERSION_FILE = "src/lcpp_lib/__version__.py"
SEMVER_FILE = "downloads/ver.txt"
NIGHTLY_FILE = "downloads/nightly-tag.txt"


def get_current_version():
    if not os.path.exists(VERSION_FILE):
        return None
    with open(VERSION_FILE, "r") as f:
        content = f.read()
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    return match.group(1) if match else None


def parse_semver(version):
    """Extract the semver part (e.g. '1.0.0') from '1.0.0b12345' or 'v1.0.0'."""
    if not version:
        return None
    match = re.search(r"(\d+\.\d+\.\d+)", version)
    return match.group(1) if match else None


def read_tag_file(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read().strip()
    return None


def read_latest_tags():
    """Read the version files written by get_download_tag.py --save."""
    semver = read_tag_file(SEMVER_FILE)
    nightly = read_tag_file(NIGHTLY_FILE)
    if not semver or not nightly:
        print(
            "Error: Version files not found. Run get_download_tag.py --save first."
        )
        sys.exit(1)
    return semver, nightly


def main():
    semver, nightly = read_latest_tags()
    current_ver = get_current_version()

    current_semver = parse_semver(current_ver)
    latest_semver = parse_semver(semver)

    print(f"Current local version: {current_ver}")
    print(f"Latest upstream semver: {latest_semver}")
    print(f"Latest upstream nightly: {nightly}")

    updated = "true" if current_semver != latest_semver else "false"

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"updated={updated}\n")
            f.write(f"version={latest_semver}\n")
            f.write(f"nightlytag={nightly}\n")

    print(f"Updated: {updated}")


if __name__ == "__main__":
    main()
