#!/bin/bash

python3 buildscripts/extract.py --clean && \
  python3 buildscripts/extract.py --build ubuntu-x64-vulkan && \
  uv build --wheel && \
  uv run auditwheel repair dist/lcpp_lib-*.whl -w wheels/ \
    --exclude libvulkan.so.* --exclude libgomp.so.* && \
  rm -f dist/lcpp_lib-*.whl
