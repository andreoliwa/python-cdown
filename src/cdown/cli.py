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
from typing import Optional

import click

from cdown import CodeOwnersFile


@click.group()
@click.option(
    "--project",
    "-p",
    type=click.Path(exists=True, dir_okay=True, file_okay=False, resolve_path=True),
    help="Path to project root",
)
def code_owners_cli(project):
    """Tools for CODEOWNERS files."""


def get_project(ctx: click.Context) -> Optional[Path]:
    project = None
    if ctx.parent:
        project = ctx.parent.params["project"]
    return Path(project) if project else None


@code_owners_cli.command()
@click.pass_context
def ls_owners(context):
    """List owners alphabetically."""
    for owner in CodeOwnersFile(get_project(context)).list_owners():
        click.echo(owner)


@code_owners_cli.command()
@click.argument("names", nargs=-1, required=False)
@click.pass_context
def ls_files(context, names):
    """List files and its owners; input one or multiple names to filter files."""
    for file in CodeOwnersFile(get_project(context)).list_files(*names):
        click.echo(file)
