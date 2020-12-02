import re
import sys
import readline

from prompt_toolkit import prompt as ptk_prompt
# from prompt_toolkit import print_formatted_text as ptk_print
# from prompt_toolkit.formatted_text import HTML, to_formatted_text

from mg.ansi import to_ansi_code, UnknownANSIKeywordException

std_print = print
std_input = input


# Configure this module using these globals (TODO: use a class, duh)

def config(
        output_enabled=sys.stdout.isatty(),
        # input_enabled=sys.stdin.isatty(), # unused
        # color_support_bits=8,             # other not yet implemented
        error_on_tags=False,
    ):
    # declare globals
    global GLOBAL_OUTPUT_ENABLED
    # global GLOBAL_INPUT_ENABLED
    # global GLOBAL_COLOR_SUPPORT_BITS
    global GLOBAL_ERROR_ON_TAGS

    # update globals
    GLOBAL_OUTPUT_ENABLED = output_enabled
    # GLOBAL_INPUT_ENABLED = input_enabled
    # GLOBAL_COLOR_SUPPORT_BITS = color_support_bits
    GLOBAL_ERROR_ON_TAGS = error_on_tags
config()


def print(*args, **kwargs):
    if GLOBAL_OUTPUT_ENABLED:
        args = [to_ansi(arg) for arg in args]
        return std_print(*args, **kwargs)
    else:
        args = [strip_ansi(arg) for arg in args]
        return std_print(*args, **kwargs)

def input(prompt, r=None):
    if sys.stdin.isatty():
        return ptk_prompt(prompt + " ", rprompt=r)
    else:
        if r is not None:
            print(r)
        return std_input(prompt + " ")



formattag = re.compile(r"<([^><]+)>")
def to_ansi(s):
    return formattag.sub(to_ansi_tag_match, str(s))

def to_ansi_tag_match(match):
    a = match[1].lower()
    # escaped <, >:
    if a.lower() == 'lt':
        return "<"
    if a == "gt":
        return ">"
    # otherwise convert to ANSI if possible:
    try:
        return to_ansi_code(a)
    except UnknownANSIKeywordException:
        if GLOBAL_ERROR_ON_TAGS:
            # raise an exception about the tag
            raise StringMarkupException(match[0])
        else:
            # silently pass over the tag
            return match[0]


def strip_ansi(s):
    return formattag.sub(no_ansi_tag_match, str(s))

def no_ansi_tag_match(match):
    a = match[1].lower()
    # escaped <, >:
    if a.lower() == 'lt':
        return "<"
    if a == "gt":
        return ">"
    # otherwise convert to ANSI if possible:
    try:
        to_ansi_code(a)
        return ""
    except UnknownANSIKeywordException:
        if GLOBAL_ERROR_ON_TAGS:
            # raise an exception about the tag
            raise StringMarkupException(match[0])
        else:
            # silently pass over the tag
            return match[0]

class StringMarkupException(Exception):
    """Unknown tag or similar formatted string error"""
