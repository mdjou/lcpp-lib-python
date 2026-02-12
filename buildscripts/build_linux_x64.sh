#!/bin/bash

uv build --wheel && \
  uv run auditwheel repair dist/lcpp_lib-*-none-any.whl -w wheels/ && \
  rm -f dist/lcpp_lib-*-none-any.whl
