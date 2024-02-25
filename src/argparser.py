# Modules
import utils

# Standard
import argparse
from typing import List, Any, Dict


class ArgParser:
    # Generic class to get arguments from the terminal
    def __init__(self, title: str, argdefs: List[Dict[str, Any]], aliases: Dict[str, List[str]], obj: Any):
        parser = argparse.ArgumentParser(description=title)

        for item in argdefs:
            name = item["name"]

            if name == "string_arg":
                names = [name]
            else:
                names = [f"--{name}", f"-{name}"]

                if name in aliases:
                    names += aliases[name]

            opts = ["type", "choices", "help", "action"]
            tail = {key: item[key] for key in opts if key in item}

            parser.add_argument(*names, **tail)

        self.args = parser.parse_args()
        self.obj = obj

    def get_list(self, attr: str, value: str, vtype: Any, separator: str) -> List[Any]:
        try:
            lst = list(map(vtype, map(str.strip, value.split(separator))))
        except:
            utils.exit(f"Failed to parse '--{attr}'")
            return []

        return lst

    def normal(self, attr: str) -> None:
        value = getattr(self.args, attr)

        if value is not None:
            setattr(self.obj, attr, value)

    def commas(self, attr: str, vtype: Any, allow_string: bool = False, is_tuple: bool = False) -> None:
        value = getattr(self.args, attr)

        if value is not None:
            if "," in value:
                lst = self.get_list(attr, value, vtype, ",")

                if is_tuple:
                    setattr(self.obj, attr, tuple(lst))
                else:
                    setattr(self.obj, attr, lst)

            elif allow_string:
                setattr(self.obj, attr, value)

    def path(self, attr: str) -> None:
        value = getattr(self.args, attr)

        if value is not None:
            setattr(self.obj, attr, utils.resolve_path(value))

    def pathlist(self, attr: str) -> None:
        value = getattr(self.args, attr)

        if value is not None:
            paths = [utils.resolve_path(p.strip()) for p in value.split(",")]
            setattr(self.obj, attr, paths)

    # Allow p1 and m1 formats
    def number(self, attr: str, vtype: Any, allow_zero: bool = False, duration: bool = False) -> None:
        default = getattr(self.obj, attr)
        value = getattr(self.args, attr)

        if value is None:
            return

        value = str(value)
        num = value
        op = ""

        if value.startswith("p") or value.startswith("m"):
            op = value[0]
            num = value[1:]

        if duration:
            num = utils.parse_duration(num)

        try:
            if vtype == int:
                num = int(num)
            elif vtype == float:
                num = float(num)
        except:
            utils.exit(f"Failed to parse '{attr}'")
            return

        if op == "p":
            num = default + num
        elif op == "m":
            num = default - num

        err = f"Value for '{attr}' is too low"

        if num == 0:
            if not allow_zero:
                utils.exit(err)
        elif num < 0:
            utils.exit(err)
            return

        setattr(self.obj, attr, num)
