"""Console script for idoit_api."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for idoit_api."""
    click.echo("Replace this message by putting your code into "
               "idoit_api.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
