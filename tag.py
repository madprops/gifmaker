#!/usr/bin/env bash

# pacman: python-gitpython
import git
import time

name = int(time.time())
repo = git.Repo(".")
repo.create_tag(name)
repo.remotes.origin.push(name)
print(f"Created tag: {name}")