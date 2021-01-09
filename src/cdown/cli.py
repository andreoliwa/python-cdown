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
from pathlib import Path

import click

from cdown import CodeOwnersFile


@click.group()
@click.option(
    "--project",
    "-p",
    type=click.Path(exists=True, dir_okay=True, file_okay=False, resolve_path=True),
    help="Path to project root",
)
def main(project):
    """Tools for CODEOWNERS files."""


@main.command()
@click.pass_context
def list_owners(ctx):
    """List owners present in the file."""
    project = None
    if ctx.parent:
        project = ctx.parent.params["project"]
    path = Path(project) if project else None
    for owner in CodeOwnersFile(path).list_owners():
        click.echo(owner)
