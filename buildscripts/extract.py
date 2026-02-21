import argparse
import glob
import os
import shutil
import tarfile
import zipfile


BUILD_UBUNTU_X64_VULKAN = "ubuntu-x64-vulkan"
BUILD_WIN_X64_VULKAN = "win-x64-vulkan"
BUILD_MACOS_ARM64 = "macos-arm64"

BUILD_CHOICES = [
    BUILD_UBUNTU_X64_VULKAN,
    BUILD_WIN_X64_VULKAN,
    BUILD_MACOS_ARM64,
]

DEST_DIR = "src/lcpp_lib/native_libs"


def get_version():
    ver_file = "downloads/ver.txt"
    if os.path.exists(ver_file):
        with open(ver_file, "r") as f:
            return f.read().strip()
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Extract and move llama.cpp libs/binaries"
    )
    parser.add_argument("--version", help="Version tag (e.g. b7903)")
    parser.add_argument(
        "--all", action="store_true", help="Move everything including binaries"
    )
    parser.add_argument(
        "--build",
        default=BUILD_UBUNTU_X64_VULKAN,
        choices=BUILD_CHOICES,
        help=f"Build type to extract. Default is {BUILD_UBUNTU_X64_VULKAN}.",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean up all possible extracted builds and exit",
    )
    args = parser.parse_args()

    dest = DEST_DIR
    if args.clean:
        if os.path.exists(dest):
            print(f"Cleaning up {dest}")
            shutil.rmtree(dest)
        print("Clean up finished.")
        return

    version = args.version or get_version()
    if not version:
        print("Error: Version not specified and downloads/ver.txt not found.")
        exit(1)

    # Find the archive in downloads/
    if args.build == BUILD_UBUNTU_X64_VULKAN:
        patterns = [f"downloads/llama-{version}-bin-ubuntu-vulkan-x64.tar.gz"]
        is_zip = False
        ostype = "linux"
    elif args.build == BUILD_WIN_X64_VULKAN:
        patterns = [f"downloads/llama-{version}-bin-win-vulkan-x64.zip"]
        is_zip = True
        ostype = "win"
    elif args.build == BUILD_MACOS_ARM64:
        patterns = [f"downloads/llama-{version}-bin-macos-arm64.tar.gz"]
        is_zip = False
        ostype = "mac"

    tarball_path = None
    for p in patterns:
        matches = glob.glob(p)
        if matches:
            tarball_path = matches[0]
            break

    if not tarball_path:
        print(f"Error: Could not find archive for version {version} and build {args.build} in downloads/")
        print(
            "Available files in downloads/:",
            os.listdir("downloads") if os.path.exists("downloads") else "none",
        )
        exit(1)

    print(f"Archive found: {tarball_path}")

    temp_extract_dir = "downloads/temp_extract"
    if os.path.exists(temp_extract_dir):
        shutil.rmtree(temp_extract_dir)
    os.makedirs(temp_extract_dir)

    print(f"Extracting to {temp_extract_dir}...")
    if is_zip:
        with zipfile.ZipFile(tarball_path, 'r') as zip_ref:
            zip_ref.extractall(temp_extract_dir)
    else:
        with tarfile.open(tarball_path, "r:gz") as tar:
            tar.extractall(path=temp_extract_dir)

    inner_items = os.listdir(temp_extract_dir)
    if len(inner_items) == 1 and os.path.isdir(
        os.path.join(temp_extract_dir, inner_items[0])
    ):
        src_base = os.path.join(temp_extract_dir, inner_items[0])
    else:
        src_base = temp_extract_dir

    if os.path.exists(dest):
        if not os.path.isdir(dest):
            print(f"Error: {dest} exists but is not a directory.")
            exit(1)
        print(f"Cleaning up destination directory: {dest}")
        shutil.rmtree(dest)

    os.makedirs(dest, exist_ok=True)

    mode_str = "Everything (Binaries + Libs)" if args.all else "Libs + License only"
    print(f"Target directory: {dest}")
    print(f"Mode: {mode_str}")

    files_moved = 0
    for root, dirs, files in os.walk(src_base):
        for item in files:
            src_path = os.path.join(root, item)

            is_lib = False
            if ostype == "mac":
                is_lib = item.endswith(".dylib") or ".dylib." in item
            elif ostype == "win":
                is_lib = item.endswith(".dll") or ".dll." in item
            else:
                is_lib = item.endswith(".so") or ".so." in item

            is_license = item.lower() == "license" or item.lower().startswith("license")

            should_move = False
            if args.all:
                should_move = True
            else:
                if is_lib or is_license:
                    should_move = True

            if should_move:
                dest_path = os.path.join(dest, item)
                
                if not os.path.exists(dest_path):
                    shutil.move(src_path, dest_path)
                    files_moved += 1
                    print(f"  Moving: {item}")
                else:
                    print(f"  Skipping duplicate: {item}")

    shutil.rmtree(temp_extract_dir)
    print(f"\nSuccess! Moved {files_moved} files to {dest}")


if __name__ == "__main__":
    main()
