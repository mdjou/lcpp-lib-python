import platform
from pathlib import Path

from .__version__ import __version__

LIB_DIR = Path(__file__).parent.resolve()


def get_lib_dir() -> Path:
    """Returns the directory containing the native libraries."""
    system = platform.system()
    if system == "Linux":
        return LIB_DIR / "linux-vulkan-x64"
    raise RuntimeError(f"Unsupported platform: {system}")


def get_lib_path() -> Path:
    """Returns the path to the main llama library."""
    system = platform.system()
    if system == "Linux":
        return get_lib_dir() / "libllama.so"
    raise RuntimeError(f"Unsupported platform: {system}")


__all__ = ["get_lib_dir", "get_lib_path", "__version__"]
