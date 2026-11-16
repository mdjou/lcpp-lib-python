## Project Description

Repackage of [Llama.cpp](https://github.com/ggml-org/llama.cpp) libraries for python ecosystem.

This package contains no python bindings, no API, and no extra abstractions. Only the compiled libraries.


## Usage

```python
import lcpp_lib

# path to directory where shared libraries are located
lcpp_lib_dir = lcpp_lib.get_lib_dir()

# path to libllama.so shared library
lcpp_lib_path = lcpp_lib.get_lib_path()

# ... (write your own bindings)
```


## Platforms

- Linux x64 (Vulkan)
- Windows x64 (Vulkan)
- macOS arm64

