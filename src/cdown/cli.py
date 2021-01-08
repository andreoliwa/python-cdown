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
@click.option(
    "--file",
    "-f",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True),
    help="Path to CODEOWNERS file",
)
def main(file):
    """Tools for CODEOWNERS files."""


@main.command()
@click.pass_context
def list_owners(ctx):
    """List owners present in the file."""
    file = ctx.parent.params["file"] if ctx.parent else None
    for owner in CodeOwnersFile(file_path=file).list_owners():
        click.echo(owner)
