#!/usr/bin/env bash
# This is used to test if the program is working properly

root="$(dirname "$(readlink -f "$0")")"
parent="$(dirname "$root")"
cd "$parent"

venv/bin/python -m gifmaker.main --script "scripts/test.toml"