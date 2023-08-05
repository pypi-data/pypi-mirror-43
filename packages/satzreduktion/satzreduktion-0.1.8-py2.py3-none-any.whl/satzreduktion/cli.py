# -*- coding: utf-8 -*-

"""Console script for satzreduktion."""
import sys
import click
from satzreduktion import *


@click.command()
@click.option(
    '--input_text',
    prompt='Welchen Text willst du reduzieren?(Pfad)',
    help='Einzulesende Textdatei'
)
@click.option(
    '--output_textname',
    prompt='Wie soll der reduzierte Text heißen?',
    help='Auszulesende Textdatei'
)
def main_1(input_text, output_textname):
    """Console script for satzreduktion."""
    click.echo("Starte Satzreduktion:")
    main(input_text, output_textname)
    return 0


if __name__ == "__main__":
    sys.exit(main_1())  # pragma: no cover
