#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from . import parse_file
import pprint

if __name__ == "__main__":
    if not len(sys.argv)>1:
        print("\n- missing path to solidity file.\n")
        print("#> python -m solidity_parser <solidity file>")
        sys.exit(1)

    node = parse_file(sys.argv[1])
    pprint.pprint(node)
