#!/bin/bash
set -e
xelatex main
biber main
xelatex main
xelatex main
