import argparse
import json
import os
import urllib.request

REPO = "ggml-org/llama.cpp"
DOWNLOAD_DIR = "downloads"
VERSION_FILE = os.path.join(DOWNLOAD_DIR, "ver.txt")

BUILD_UBUNTU_X64_VULKAN = "ubuntu-x64-vulkan"
BUILD_WIN_X64_VULKAN = "win-x64-vulkan"
BUILD_WIN_X64_CUDA_12 = "win-x64-cuda-12"
BUILD_WIN_X64_CUDA_13 = "win-x64-cuda-13"
BUILD_WIN_X64_CUDA_12_CUDART = "win-x64-cuda-12-cudart"
BUILD_WIN_X64_CUDA_13_CUDART = "win-x64-cuda-13-cudart"
BUILD_MACOS_ARM64 = "macos-arm64"

BUILD_CHOICES = [
    BUILD_UBUNTU_X64_VULKAN,
    BUILD_WIN_X64_VULKAN,
    BUILD_WIN_X64_CUDA_12,
    BUILD_WIN_X64_CUDA_13,
    BUILD_WIN_X64_CUDA_12_CUDART,
    BUILD_WIN_X64_CUDA_13_CUDART,
    BUILD_MACOS_ARM64,
]


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
    parser = argparse.ArgumentParser(description="Download llama.cpp release")
    parser.add_argument(
        "--version",
        help="Version tag (e.g. b7903). If not provided, reads from downloads/ver.txt",
    )
    parser.add_argument(
        "--build",
        default=BUILD_UBUNTU_X64_VULKAN,
        choices=BUILD_CHOICES,
        help=f"Build type to download. Default is {BUILD_UBUNTU_X64_VULKAN}.",
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

    assets = release.get("assets", [])
    target_asset = None
    for asset in assets:
        name = asset["name"]
        lower_name = name.lower()
        if args.build == BUILD_UBUNTU_X64_VULKAN:
            if (
                "ubuntu" in lower_name
                and "vulkan" in lower_name
                and "x64" in lower_name
                and lower_name.endswith(".tar.gz")
            ):
                target_asset = asset
                break
        elif args.build == BUILD_WIN_X64_VULKAN:
            if (
                "win" in lower_name
                and "vulkan" in lower_name
                and "x64" in lower_name
                and lower_name.endswith(".zip")
            ):
                target_asset = asset
                break
        elif args.build == BUILD_WIN_X64_CUDA_12:
            if (
                "win" in lower_name
                and "cuda-12" in lower_name
                and "cudart" not in lower_name
                and "x64" in lower_name
                and lower_name.endswith(".zip")
            ):
                target_asset = asset
                break
        elif args.build == BUILD_WIN_X64_CUDA_13:
            if (
                "win" in lower_name
                and "cuda-13" in lower_name
                and "cudart" not in lower_name
                and "x64" in lower_name
                and lower_name.endswith(".zip")
            ):
                target_asset = asset
                break
        elif args.build == BUILD_WIN_X64_CUDA_12_CUDART:
            if (
                "win" in lower_name
                and "cudart" in lower_name
                and "cuda-12" in lower_name
                and "x64" in lower_name
                and lower_name.endswith(".zip")
            ):
                target_asset = asset
                break
        elif args.build == BUILD_WIN_X64_CUDA_13_CUDART:
            if (
                "win" in lower_name
                and "cudart" in lower_name
                and "cuda-13" in lower_name
                and "x64" in lower_name
                and lower_name.endswith(".zip")
            ):
                target_asset = asset
                break
        elif args.build == BUILD_MACOS_ARM64:
            if (
                "macos" in lower_name
                and "arm64" in lower_name
                and lower_name.endswith(".tar.gz")
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
            f"Could not find a matching release asset for version {version} and build {args.build}."
        )
        exit(1)


if __name__ == "__main__":
    main()
