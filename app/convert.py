import argparse
import re
from functools import cached_property
import difflib


class Converter:
    @cached_property
    def args(self) -> argparse.Namespace:
        parser = argparse.ArgumentParser(
            description="Apply fixes to ART names to JSON files")
        parser.add_argument("--input-file", type=str, required=True,
                            help="JSON file")
        parser.add_argument("--output-file", type=str,
                            help="Name for output file (otherwise overrides input)")
        parser.add_argument("--print-diff", action="store_true",
                            help="Print the applied changes")
        parser.add_argument("--confirm-save", action="store_true",
                            help="Ask for confirmation before saving")

        args = parser.parse_args()
        if args.output_file == None:
            args.output_file = args.input_file
        return args

    @property
    def regexes(self) -> dict[re.Pattern, str]:
        return {
            # Output channel
            re.compile(r"(\"(56)\"((?!55).)+?)(?=(phaseSelectChannel0output))(\w+)", flags=re.DOTALL): r"\1phaseSelectChannel2output",
            re.compile(r"(\"(56)\"((?!55).)+?)(?=(phaseSelectChannel1output))(\w+)", flags=re.DOTALL): r"\1phaseSelectChannel3output",
            re.compile(r"(\"(57)\"((?!55).)+?)(?=(phaseSelectChannel0output))(\w+)", flags=re.DOTALL): r"\1phaseSelectChannel4output",
            re.compile(r"(\"(57)\"((?!55).)+?)(?=(phaseSelectChannel1output))(\w+)", flags=re.DOTALL): r"\1phaseSelectChannel5output",
            re.compile(r"(\"(58)\"((?!55).)+?)(?=(phaseSelectChannel0output))(\w+)", flags=re.DOTALL): r"\1phaseSelectChannel6output",
            re.compile(r"(\"(58)\"((?!55).)+?)(?=(phaseSelectChannel1output))(\w+)", flags=re.DOTALL): r"\1phaseSelectChannel7output",
            # Mask
            re.compile(r"(\"(10)\"((?!09).)+?)(?=(cfg_din_mask\[7:0\]))(\w+\[7:0\])", flags=re.DOTALL): r"\1cfg_din_mask[15:8]",
            re.compile(r"(\"(11)\"((?!09).)+?)(?=(cfg_din_mask\[7:0\]))(\w+\[7:0\])", flags=re.DOTALL): r"\1cfg_din_mask[23:16]",
            re.compile(r"(\"(12)\"((?!09).)+?)(?=(cfg_din_mask\[7:0\]))(\w+\[7:0\])", flags=re.DOTALL): r"\1cfg_din_mask[31:24]",
            # muz
            re.compile(r"muzEn1to8"): "muxEn1to8",
        }

    @cached_property
    def input_text(self) -> str:
        with open(self.args.input_file, "r") as f:
            return f.read()

    @cached_property
    def output_text(self) -> str:
        output = self.input_text
        for regex, replacement in self.regexes.items():
            output = regex.sub(replacement, output)
        return output

    @cached_property
    def diff(self) -> difflib.Differ:
        return difflib.ndiff(self.input_text.splitlines(keepends=True), self.output_text.splitlines(keepends=True))

    @cached_property
    def filter_diff(self) -> list[str]:
        diff = [line for line in self.diff if not line.startswith("?")]
        margin = 3
        def accept(line_number):
            for i in range(max(0, line_number - margin), min(len(diff), line_number + margin)):
                if diff[i].startswith("+") or diff[i].startswith("-"):
                    return True
            return False
        
        diff = [line for line_number, line in enumerate(diff) if accept(line_number)]
        return diff

    def print_diff(self) -> None:
        print(''.join(self.filter_diff), end="")

    def confirmation(self) -> bool:
        if self.args.input_file == self.args.output_file:
            answer = input("Apply changes to {} (override file): Y/n ".format(self.args.input_file))
        else:
            answer = input("Save changes to {} to {}: Y/n ".format(self.args.input_file, self.args.output_file))
            
        if answer.lower() in ["y","yes", ""]:
            return True
        elif answer.lower() in ["n","no"]:
            return False
        else:
            return self.confirmation()

    def save(self):
        with open(self.args.output_file, "w") as f:
            f.write(self.output_text)

    def run(self):
        if self.input_text == self.output_text:
            print("No changes")
            return
        if self.args.print_diff:
            self.print_diff()
        if self.args.confirm_save:
            if not self.confirmation():
                print("Aborted")
                return
        self.save()

def main():
    c = Converter()
    c.run()

if __name__ == "__main__":
    main()