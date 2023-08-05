# -*- coding: utf-8 -*-

"""Console script for satzreduktion."""
import sys
import click
import satzreduktion


@click.command()
def main(args=None):
    """Console script for satzreduktion."""
    click.echo("Replace this message by putting your code into "
               "satzreduktion.cli.main")
    satzreduktion.main()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
