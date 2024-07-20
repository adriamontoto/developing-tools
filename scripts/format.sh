#!/bin/sh -e
set -x

wget https://raw.githubusercontent.com/adriamontoto/dotfiles/master/python/ruff.toml --output-document /tmp/ruff.toml

ruff check developing_tools tests --fix-only --config /tmp/ruff.toml
ruff format developing_tools tests --config /tmp/ruff.toml
