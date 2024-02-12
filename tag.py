#!/usr/bin/env python

# This is used to create a tag in the git repo
# You probably don't want to run this

# pacman: python-gitpython
import git
import time

name = int(time.time())
repo = git.Repo(".")
repo.create_tag(name)
repo.remotes.origin.push(name)
print(f"Created tag: {name}")