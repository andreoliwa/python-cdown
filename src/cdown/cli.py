"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mcdown` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``cdown.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``cdown.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import click

from cdown import CodeOwnersFile


@click.group()
def main():
    """Tools for CODEOWNERS files."""


@main.command()
def list_owners():
    """List owners present in the file."""
    for owner in CodeOwnersFile().list_owners():
        click.echo(owner)
