#!/bin/bash

python3 buildscripts/extract.py --clean && \
  python3 buildscripts/extract.py --build macos-arm64 && \
  uv build --wheel && \
  mv dist/lcpp_lib-*-macosx_11_0_arm64.whl wheels/
