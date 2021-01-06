#!/bin/env python3
import sys
from depends_graph import DependsGraph


def menu(args):
    print(f"Usage: {args[0]} args...\n" \
            "args:\n" \
            "\t app_name - x\n" \
            "\t x - depend_app_name\n" \
            "\t x - ?")


def main(args):
    if len(args) != 4:
        menu(args)
        return
    
    base = args[1]
    depends = args[3]
    unknown = 'x'

    graph = DependsGraph.instance()

    if base == unknown and depends == unknown:
        print(graph)
    elif base is not unknown:
        print(f"{base}:\n\t{graph.get_depends(base)}")
    elif depends is not unknown:
        print(f"{depends}:\n\t{graph.get_base(depends)}")


if __name__ == '__main__':
    main(sys.argv)


