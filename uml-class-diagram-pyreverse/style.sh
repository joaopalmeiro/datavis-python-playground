#!/bin/bash

# sh style.sh

pyreverse OOP.py --filter-mode=ALL
python3 style_uml_class_diagram.py
dot -Tpng -Gdpi=300 classes.dot -o uml.png
