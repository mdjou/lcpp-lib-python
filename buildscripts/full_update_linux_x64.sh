#!/bin/bash

python3 buildscripts/get_repo_latest_version.py --save && \
  python3 buildscripts/update_project_version.py && \
  python3 buildscripts/download_linux_vulkan.py && \
  python3 buildscripts/extract_linux_vulkan.py && \
  buildscripts/build_linux_x64.sh
