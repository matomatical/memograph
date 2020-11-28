def colormap_red_green(p):
    red = format(int(255*(1-p)), "02x")
    grn = format(int(255*p),     "02x")
    blu = "00"
    return f"#{red}{grn}{blu}"
