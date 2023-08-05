import click
import pprint

from .mailgun import Mailgun


@click.group()
def main():
    pass

@click.command()
def routes():
    """list all routes"""
    api = Mailgun()
    pprint.pprint(api.get_routes())

main.add_command(routes)

if __name__ == '__main__':
    main()
