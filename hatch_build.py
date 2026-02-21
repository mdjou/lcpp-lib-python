import os
from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        build_data["pure_python"] = False

        if os.path.exists("src/lcpp_lib/native_libs/llama.dll"):
            plat = "win_amd64"
            build_data["tag"] = f"py3-none-{plat}"
        if os.path.exists("src/lcpp_lib/native_libs/libllama.dylib"):
            plat = f"macosx_11_0_arm64"
            build_data["tag"] = f"py3-none-{plat}"
        if os.path.exists("src/lcpp_lib/native_libs/libllama.so"):
            # linux naming will be further fixed by auditwheel as a post-build step
            plat = f"linux_x86_64"
            build_data["tag"] = f"py3-none-{plat}"

