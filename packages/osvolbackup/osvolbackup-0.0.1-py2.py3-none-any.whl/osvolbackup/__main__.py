from .cli.server import server
from .cli import version
import click


@click.group()
@click.version_option(version=version)
def cli():
    pass


cli.add_command(server)


def main():
    cli()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise
