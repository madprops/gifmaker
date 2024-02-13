#!/usr/bin/env bash
# This is used to test if borat is working properly

root="$(dirname "$(readlink -f "$0")")"
parent="$(dirname "$root")"
cd "$parent"

venv/bin/python src/borat.py --script="scripts/test.toml"