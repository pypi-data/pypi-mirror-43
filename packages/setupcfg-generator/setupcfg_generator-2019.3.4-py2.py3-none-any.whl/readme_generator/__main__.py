#!/usr/bin/env python
"""generate README"""
import click
import readme_generator


MODULE_NAME = "readme_generator"
PROG_NAME = 'python -m %s' % MODULE_NAME
USAGE = 'python -m %s folder ...' % MODULE_NAME


@click.command()
@click.argument('folder', required=False)
def _cli(folders):
    readme_generator.create(path)


if __name__ == '__main__':
    _cli(prog_name=PROG_NAME)
