#!/usr/bin/env python3
"""
Generate random data for your application
"""

import argparse
import importlib
import logging


def add_args():
    parser = argparse.ArgumentParser(
        description="Generate random data for your application"
    )
    parser.add_argument("-w", "--writer", type=str, default="stdout")
    parser.add_argument("-f", "--format", type=str, default="json")
    parser.add_argument("-c", "--count", type=int, default=1)
    parser.add_argument("-v", "--verbose", action="store_true")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-t", "--template", type=str)
    group.add_argument(
        "-i", "--items", type=str, action="append", metavar="KEY=VALUE"
    )
    return parser


def init_logging(verbose: bool = False) -> logging.Logger:
    level = logging.DEBUG if verbose else logging.ERROR
    logging.basicConfig(
        format="%(levelname)-9s %(funcName)s:%(lineno)d - %(message)s",
        datefmt="%H:%M:%S",
        level=level,
    )
    return logging.getLogger()


def main() -> None:
    from echolalia.generator import Generator

    parser = add_args()
    args, _ = parser.parse_known_args()

    writer_name = args.writer
    formatter_name = args.format

    writer_mod = importlib.import_module(f"echolalia.writer.{writer_name}")
    writer = writer_mod.Writer()
    parser = writer.add_args(parser)

    formatter_mod = importlib.import_module(f"echolalia.formatter.{formatter_name}er")
    formatter = formatter_mod.Formatter()
    parser = formatter.add_args(parser)

    args = parser.parse_args()
    log = init_logging(verbose=args.verbose)
    log.debug("Start")

    template = args.template
    count = args.count

    if template is None:
        log.debug("Generating %d docs with %d item(s)", count, len(args.items))
        items: dict[str, str] = {}
        for item in args.items:
            kv = item.split("=", 1)
            if len(kv) == 2:
                items[kv[0]] = kv[1]
            else:
                items[item] = item
        generator = Generator(items=items)
    else:
        log.debug("Generating %d docs with template %s", count, template)
        generator = Generator(template=template)

    data = generator.generate(count)

    log.debug('Marshalling with formatter "%s"', args.format)
    docs = formatter.marshall(args, data)

    log.debug('Writing with writer "%s"', args.writer)
    writer.write(args, docs)

    log.debug("Done")
    parser.exit(status=0)


if __name__ == "__main__":
    main()
