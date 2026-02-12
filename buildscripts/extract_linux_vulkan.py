import argparse
import glob
import os
import shutil
import tarfile


def get_version():
    ver_file = "downloads/ver.txt"
    if os.path.exists(ver_file):
        with open(ver_file, "r") as f:
            return f.read().strip()
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Extract and move llama.cpp vulkan libs/binaries"
    )
    parser.add_argument("--version", help="Version tag (e.g. b7903)")
    parser.add_argument(
        "--all", action="store_true", help="Move everything including binaries"
    )
    parser.add_argument(
        "--dest",
        default="src/lcpp_lib/linux-vulkan-x64",
        help="Destination directory (default: vulkan/)",
    )
    args = parser.parse_args()

    version = args.version or get_version()
    if not version:
        print("Error: Version not specified and downloads/ver.txt not found.")
        exit(1)

    # Find the tarball in downloads/
    # Flexible pattern matching to account for naming variations
    patterns = [
        f"downloads/llama-{version}-bin-ubuntu-vulkan-x64.tar.gz",
    ]

    tarball_path = None
    for p in patterns:
        matches = glob.glob(p)
        if matches:
            tarball_path = matches[0]
            break

    if not tarball_path:
        print(f"Error: Could not find tarball for version {version} in downloads/")
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
    with tarfile.open(tarball_path, "r:gz") as tar:
        tar.extractall(path=temp_extract_dir)

    # Find the source directory (usually llama-<version>)
    inner_items = os.listdir(temp_extract_dir)
    if len(inner_items) == 1 and os.path.isdir(
        os.path.join(temp_extract_dir, inner_items[0])
    ):
        src_base = os.path.join(temp_extract_dir, inner_items[0])
    else:
        src_base = temp_extract_dir

    if os.path.exists(args.dest):
        if not os.path.isdir(args.dest):
            print(f"Error: {args.dest} exists but is not a directory.")
            exit(1)
        print(f"Cleaning up destination directory: {args.dest}")
        shutil.rmtree(args.dest)

    os.makedirs(args.dest, exist_ok=True)

    mode_str = "Everything (Binaries + Libs)" if args.all else "Libs + License only"
    print(f"Target directory: {args.dest}")
    print(f"Mode: {mode_str}")

    files_moved = 0
    for item in os.listdir(src_base):
        src_path = os.path.join(src_base, item)
        if os.path.isdir(src_path):
            continue

        is_lib = item.endswith(".so") or ".so." in item
        is_license = item.lower() == "license" or item.lower().startswith("license")

        should_move = False
        if args.all:
            should_move = True
        else:
            if is_lib or is_license:
                should_move = True

        if should_move:
            dest_path = os.path.join(args.dest, item)
            shutil.move(src_path, dest_path)
            files_moved += 1
            print(f"  Moving: {item}")

    shutil.rmtree(temp_extract_dir)
    print(f"\nSuccess! Moved {files_moved} files to {args.dest}")


if __name__ == "__main__":
    main()
