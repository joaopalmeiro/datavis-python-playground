from graphviz import Source
import re
import argparse


def add_style(filename: str) -> str:
    FONTNAME = "Roboto-Regular"
    FONTCOLOR = "#2F2F2F"
    SHAPECOLOR = "#2F2F2F"

    MARK = '"'

    style = fr"\1color={MARK}{SHAPECOLOR}{MARK}, fontname={MARK}{FONTNAME}{MARK}, fontcolor={MARK}{FONTCOLOR}{MARK}, "

    s = Source.from_file(filename).source

    s = re.sub(r"(\[)(?=label)", style, s)

    with open(filename, "w") as dot_file:
        dot_file.write(s)

    return "\n\N{sparkles} \N{memo} Done! \N{sparkles}\n"


if __name__ == "__main__":
    FILENAME = "classes.dot"

    parser = argparse.ArgumentParser(
        description="Style the UML class diagram generated with Pyreverse.",
        epilog="Powered by Graphviz and Pyreverse.",
    )

    parser.add_argument(
        "-f",
        "--filename",
        help="The filename of the UML class diagram DOT file.",
        default=FILENAME,
    )

    args = parser.parse_args()

    print(add_style(args.filename))
