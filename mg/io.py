import re
import os
import sys
import readline                  # enable richer prompts with navigation
readline.set_auto_history(False) # but disable history

std_print = print
std_input = input


def print(*args, **kwargs):
    args = [to_ansi(arg) for arg in args]
    return std_print(*args, **kwargs)


def input(prompt, r=None):
    prompt = to_ansi(prompt)
    if r is not None:
        cols = os.get_terminal_size().columns
        prompt = format(to_ansi(r), f">{cols}s") + '\r' + prompt
    return std_input(prompt + " ")
    # TODO: Backspacing wipes rprompt, which is not redrawn



# # # # # # # #
# CONFIGURATION
# 

def config(
        output_enabled=sys.stdout.isatty(),
        # color_support_bits=8,             # other not yet implemented
        error_on_tags=False,
    ):
    # declare globals
    global GLOBAL_OUTPUT_ENABLED
    # global GLOBAL_COLOR_SUPPORT_BITS
    global GLOBAL_ERROR_ON_TAGS

    # update globals
    GLOBAL_OUTPUT_ENABLED = output_enabled
    # GLOBAL_COLOR_SUPPORT_BITS = color_support_bits
    GLOBAL_ERROR_ON_TAGS = error_on_tags
config()


# # # # # # # #
# STRING MARKUP
# 
# The following functions help convert text with markup tags to text with (or
# without) ANSI escape codes.
# 
# For example:
# 
# >>> print(to_ansi("<red>Hello, world!<reset>"))
# \033[31mHello, world!\033[0m
# >>> config(output_enabled=False)
# >>> print(no_ansi("<red>Hello, world!<reset>"))
# Hello, world!
# 


from mg.ansi import to_ansi_code, UnknownANSIKeywordException


TAG = re.compile(r"<([^><]+)>")


def to_ansi(s):
    return TAG.sub(to_ansi_tag_match, str(s))


def to_ansi_tag_match(match):
    a = match[1].lower()
    # escaped <, >:
    if a.lower() == 'lt':
        return "<"
    if a == "gt":
        return ">"
    # otherwise convert to ANSI if possible:
    try:
        ansicode = to_ansi_code(a)
        if GLOBAL_OUTPUT_ENABLED:
            return ansicode
        else:
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
