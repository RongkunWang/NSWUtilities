#!/usr/bin/env python3

from typing import Generic, Union
import json

class NSWConfigJSONEncoder(json.JSONEncoder):
    """A JSON Encoder that puts small containers on single lines.

    Modified from: https://gist.github.com/jannismain/e96666ca4f059c3e5bc28abb711b5c92
    """

    CONTAINER_TYPES = (list, tuple, dict)
    """Container datatypes include primitives or other containers."""

    MAX_WIDTH = 78
    """Maximum width of a container that might be put on a single line."""

    MAX_ITEMS = 8
    """Maximum number of items in container that might be put on single line."""

    def __init__(self, *args, **kwargs):
        # using this class without indentation is pointless
        if kwargs.get("indent") is None:
            kwargs.update({"indent": 4})
        super().__init__(*args, **kwargs)
        self.indentation_level = 0

    def encode(self, o, array_length=8):
        """Encode JSON object *o* with respect to single line lists."""
        if isinstance(o, (list, tuple)):
            if self._put_on_single_line(o):
                return "[" + ", ".join(self.encode(el) for el in o) + "]"
            else:
                self.indentation_level += 1
                lines = []
                idx = 0
                for block in range(len(o) // array_length):
                    idx = (block * array_length) + array_length
                    lines.append(
                        self.indent_str + ",".join(map(str, o[block * array_length : idx])))
                if idx != len(o):
                    lines.append(
                        self.indent_str + ",".join(map(str, o[idx : ])))
                self.indentation_level -= 1
                return "[\n" + ",\n".join(lines) + "\n" + self.indent_str + "]"
        elif isinstance(o, dict):
            if o:
                self.indentation_level += 1
                output = [
                    self.indent_str + f"{json.dumps(k)}: {self.encode(v)}"
                    for k, v in o.items()
                ]
                self.indentation_level -= 1
                return "{\n" + ",\n".join(output) + "\n" + self.indent_str + "}"
            else:
                return "{}"
        elif isinstance(o, bool):
            return json.dumps(o)
        elif isinstance(o, int):
            return format(o, "d")
        elif isinstance(o, float):
            return format(o, "g")
        elif isinstance(o, str):
            o = o.replace("\n", "\\n")  # escape newlines
            o = o.replace("\/", "/")  # unescape slashes
            if o.isnumeric():
                try:
                    return format(int(o), "d")
                except ValueError as e:
                    pass
            else:
                try:
                    return format(float(o), "g")
                except ValueError as e:
                    pass
            return f'"{o}"'
        else:
            # return json.dumps(o)
            super(NSWConfigJSONEncoder, self).default(o)

    def iterencode(self, o, **kwargs):
        """Required to also work with `json.dump`."""
        return self.encode(o)

    def _put_on_single_line(self, o):
        return (
            self._primitives_only(o)
            and len(o) <= self.MAX_ITEMS
            and len(str(o)) - 2 <= self.MAX_WIDTH
        )

    def _primitives_only(self, o: Union[list, tuple]):
        if isinstance(o, (list, tuple)):
            return not any(isinstance(el, self.CONTAINER_TYPES) for el in o)
        elif isinstance(o, dict):
            return not any(isinstance(el, self.CONTAINER_TYPES) for el in o.values())

    @property
    def indent_str(self) -> str:
        if isinstance(self.indent, int):
            return " " * (self.indentation_level * self.indent)
        elif isinstance(self.indent, str):
            return self.indentation_level * self.indent
        else:
            raise ValueError(
                f"indent must either be of type int or str (is: {type(self.indent)})"
            )
