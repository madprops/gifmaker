from setuptools import setup, find_packages
import json

with open("gifmaker/manifest.json", "r") as file:
    manifest = json.load(file)

title = manifest["title"]
program = manifest["program"]
version = manifest["version"]

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

package_data = {}
package_data[program] = ["fonts/*.ttf", "*.txt", "*.json"]

setup(
    name = title,
    version = version,
    install_requires=requirements,
    packages = find_packages(where="."),
    package_dir = {"": "."},
    package_data = package_data,
    entry_points = {
        "console_scripts": [
            f"{program}={program}.main:main",
        ],
    },
)
