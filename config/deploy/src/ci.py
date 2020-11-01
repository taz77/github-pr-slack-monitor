#!/usr/bin/env python
import argparse
import sys
import os
from mako.template import Template


def main(arguements):
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--outfile', help="Output file",
                            default=sys.stdout, type=argparse.FileType('w'))
    parser.parse_args()
    args = parser.parse_args(arguements)

    print(args)
    template = open('compose.yml.tpl', 'r')




if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))