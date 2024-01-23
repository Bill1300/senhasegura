#!/bin/bash
argsterminal=""
for arg in "$@"; do
    argsterminal="$argsterminal $arg"
done
python3 ~/.senhasegura/start.py $argsterminal