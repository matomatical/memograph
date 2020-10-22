"""
Simplified higher-level frontend to subprocess and Popen with options useful
to me for easily executing foreground (w/ io) or background (no io) procs.
"""

import os
import subprocess

class NonZeroExitCode(Exception):
    """A subprocess exits with non-zero return code."""

def background(*argv, setpgrp=False):
    subprocess.Popen(
        argv,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setpgrp if setpgrp else (lambda: None),
    )
    # return (nothing) immediately

def foreground(argv, stdin_data=None, allow_err=False):
    p = subprocess.Popen(
        argv,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        text=True
    )
    # await the process, capture output
    out, err = p.communicate(stdin_data)
    rc = p.returncode
    if rc or (err and not allow_err):
        raise NonZeroExitCode(
            f"Program exited with code: {rc}\n"
            f"==> stdout <==\n{out}\n"
            f"==> stderr <==\n{err}"
        )
    else:
        return out
