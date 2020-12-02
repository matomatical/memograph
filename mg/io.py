import re
import sys

from prompt_toolkit import prompt as ptk_prompt
from prompt_toolkit import print_formatted_text as ptk_print
from prompt_toolkit.formatted_text import HTML, to_formatted_text

std_print = print
std_input = input
htmltag = re.compile(r"</?[^>]+>")

if sys.stdout.isatty():
    def print(*args, **kwargs):
        ptk_print(*[HTML(str(s)) for s in args], **kwargs)
else:
    def print(*args, **kwargs):
        std_print(*[htmltag.sub("", s) for s in args], **kwargs)

if sys.stdin.isatty():
    def input(prompt, r=None):
        return ptk_prompt(prompt + " ", rprompt=r)
else:
    def input(prompt, r=None):
        if r is not None:
            print(r)
        return std_input(prompt + " ")

