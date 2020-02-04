#!/bin/bash

vl2svg server-ssb-mean-duration-with-errorbars.vl.json server-ssb-mean-duration-with-errorbars.svg
cairosvg server-ssb-mean-duration-with-errorbars.svg -o server-ssb-mean-duration-with-errorbars.pdf
