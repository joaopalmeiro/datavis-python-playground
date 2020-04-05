from graphviz import Source
import re

FILENAME = "classes.dot"

FONTNAME = "Roboto-Regular"
FONTCOLOR = "#2F2F2F"

MARK = '"'

style = fr"\1fontname={MARK}{FONTNAME}{MARK}, fontcolor={MARK}{FONTCOLOR}{MARK}, "

s = Source.from_file(FILENAME).source

s = re.sub(r"(\[)(?=label)", style, s)

with open(FILENAME, "w") as dot_file:
    dot_file.write(s)
