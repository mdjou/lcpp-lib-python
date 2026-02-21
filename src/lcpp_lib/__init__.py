import platform
from pathlib import Path

from .__version__ import __version__

LIB_DIR = Path(__file__).parent.resolve()


def get_lib_dir() -> Path:
    """Returns the directory containing the native libraries."""
    return LIB_DIR / "native_libs"


def get_lib_path() -> Path:
    """Returns the path to the main llama library."""
    system = platform.system()
    if system == "Linux":
        return get_lib_dir() / "libllama.so"
    elif system == "Darwin":
        return get_lib_dir() / "libllama.dylib"
    elif system == "Windows":
        return get_lib_dir() / "llama.dll"
    raise RuntimeError(f"Unsupported platform: {system}")


__all__ = ["get_lib_dir", "get_lib_path", "__version__"]


if platform.system() == "Windows":
    lib_path = get_lib_dir()
    from os import add_dll_directory
    add_dll_directory(str(lib_path))
