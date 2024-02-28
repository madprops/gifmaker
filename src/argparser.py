# Modules
import utils

# Standard
import argparse
from typing import List, Any, Dict


class ArgParser:
    # Generic class to get arguments from the terminal
    def __init__(self, title: str, argdefs: Dict[str, Any], aliases: Dict[str, List[str]], obj: Any):
        parser = argparse.ArgumentParser(description=title)
        argdefs["string_arg"] = {"nargs": "*"}

        for key in argdefs:
            item = argdefs[key]

            if key == "string_arg":
                names = [key]
            else:
                # Add -- and - formats
                names = [f"--{key}", f"-{key}"]
                key2 = key.replace("-", "")

                # Check without dashes
                if key2 != key:
                    names.extend([f"--{key2}", f"-{key2}"])

            if key in aliases:
                names += aliases[key]

            opts = ["type", "choices", "help", "action", "nargs"]
            tail = {key: item[key] for key in opts if key in item}

            parser.add_argument(*names, **tail)

        self.args = parser.parse_args()
        self.obj = obj

    def string_arg(self) -> str:
        return " ".join(self.args.string_arg)

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
            self.set(attr, value)

    def commas(self, attr: str, vtype: Any, allow_string: bool = False, is_tuple: bool = False) -> None:
        value = getattr(self.args, attr)

        if value is not None:
            if "," in value:
                lst = self.get_list(attr, value, vtype, ",")

                if is_tuple:
                    self.set(attr, tuple(lst))
                else:
                    self.set(attr, lst)

            elif allow_string:
                self.set(attr, value)

    def path(self, attr: str) -> None:
        value = getattr(self.args, attr)

        if value is not None:
            self.set(attr, utils.resolve_path(value))

    # Allow p1 and m1 formats
    def number(self, attr: str, vtype: Any, allow_zero: bool = False, duration: bool = False) -> None:
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

        default = self.get(attr)

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

        self.set(attr, num)

    def get(self, attr: str) -> Any:
        return getattr(self.obj, attr)

    def set(self, attr: str, value: Any) -> None:
        setattr(self.obj, attr, value)
