"""Console script for idoit_api_client."""
import sys
import click

from idoit_api_client import Constants, API

@click.command()
def main(args=None):
    """Console script for idoit_api_client."""
    click.echo("Replace this message by putting your code into "
               "idoit_api_client.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")

    click.echo("Test API")
    config = {
        Constants.URL: 'https://demo.i-doit.com/src/jsonrpc.php',
        Constants.KEY: 'c1ia5q',
        Constants.USERNAME: 'admin',
        Constants.PASSWORD: 'admin'
    }
    api = API(config)
    click.echo("Test connect")
    api.connect()
    click.echo("Test login")
    result = api.login()
    click.echo("Test request")
    result = api.request('cmdb.category.read', {
        'objID': 1,
        'category': 'C__CATG__GLOBAL',
        'params': {
            'limit': 1
        }
    })
    click.echo(result)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
