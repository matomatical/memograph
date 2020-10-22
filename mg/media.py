"""
Displaying media in your terminal!

Media type | Current tool | Requirements        | Future support options
-----------+--------------+---------------------+----------------------------
   Image   | iterm2 codes | iterm2 (osx)        | viu(er)? kitty protocol?
   LaTeX   | ^, pnglatex  | iterm2 (osx), [1]   | ^, extend term w/ KaTeX?
   Sound   | ffplay       | should be on *nix   | still fork, but faster?
    TTS    | say          | osx                 | espeak, *nix alt.?
    STT    | vosk         | *nix? osx?          | open alt? train my own?

[1]: "pnglatex depends on dvipng, imagemagick, latex and optipng packages."
    Furthermore, I had to modify the script to use gsed and a few others,
    and tweak the usage of mktemp, to get it to work on osx.
"""

from mg.fgbg import foreground, background
import base64

def image(path_or_data, path=True, img_kwargs={}, print_kwargs={},
        do_print=True):
    """
    Using iterm2's special syntax, encode image data in base64 and
    (if do_print is True) print iterm2 special codes to the terminal,
    resulting in image display (else return the codes for later printing).
    
    path_or_data is treated as the path to a binary image file when path is
    True, or as a string representing binary image data when path is False

    img_kwargs may be as follows:
    Key	                    Description of value
    -------------------------------------------------------------------------
    width                   rendering width  (optional)
    height                  rendering height (optional)
    preserveAspectRatio     respect (1, default) aspect ratio
    (For reference, additional unused parameters are:)
    name                    filename for download (defaults to "Unnamed file")
    size                    max file transfer size in bytes (unused?)
    inline                  display (1) or download (0, default) file

    print_kwargs are passed to the print function used in this call (unless
    do_print is false, in which case there is no print call)
    """
    # encode data
    if path:
        data = base64.b64encode(open(path_or_data, 'rb').read()).decode()
    else:
        data = base64.b64encode(path_or_data.encode()).decode()
    # prepare and execute
    options = ";".join([f"{k}={v}" for k, v in img_kwargs.items()])
    command = "\033]1337;File=inline=1;"+options+":"+data+"\a"
    if do_print:
        print(command, **print_kwargs)
    else:
        return command

def latex(code, img_kwargs={}, print_kwargs={}):
    pass

def sound(path, detach=True):
    background('ffplay', '-nodisp', '-autoexit', path, setpgrp=detach)

def voice(text, voice=None, detach=False):
    if voice:
        background('say', '-v', voice, text, setpgrp=detach)
    else:
        background('say',              text, setpgrp=detach)

def listen():
    return ""
