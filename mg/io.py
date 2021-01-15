import re
import os
import sys
import readline                  # enable richer prompts with navigation
readline.set_auto_history(False) # but disable history

std_print = print
std_input = input


def print(*args, r=None, sep=" ", **kwargs):
    if r is not None:
        l = sep.join(to_ansi(arg) for arg in args)
        std_print(justify(l=l, r=to_ansi(r)), sep=sep, **kwargs)
    else:
        std_print(*[to_ansi(arg) for arg in args], sep=sep, **kwargs)


def input(prompt, r=None, expected_width=1):
    p = to_ansi(prompt)
    if r is not None:
        p = justify(l=p, r=to_ansi(r), padding=1+expected_width)
    return std_input(p + " ")
    # TODO: Backspacing wipes rprompt, which is not redrawn


def justify(l="", r="", padding=0):
    llen = ansi_len(l)
    rlen = ansi_len(r)
    if GLOBAL_OUTPUT_ENABLED:
        cols = os.get_terminal_size().columns
        if cols >= llen + rlen + padding:
            return "\r" + " "*(cols-rlen) + r + "\r" + l
        return "\r" + " "*(cols-rlen) + r + "\n" + l
    return r + "\n" + l

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


from mg.ansi import to_ansi_code, UnknownANSIKeywordException, ansi_len

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
