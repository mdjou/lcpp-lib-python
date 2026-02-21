#!/bin/bash

python3 buildscripts/extract.py --clean && \
  python3 buildscripts/extract.py --build win-x64-vulkan && \
  uv build --wheel && \
  mv dist/lcpp_lib-*-win_amd64.whl wheels/