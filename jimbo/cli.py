import logging
import sys

import click

import client
import config

log = logging.getLogger(__name__)


def _run(url, username, password, config_file):
    conf = config.Config()
    conf.init(config_file)

    arty = client.ArtifactoryClient(url, username, password)

    for r in conf.get_repositories():
        arty.create_or_update_repository(r["key"], r)

    actual_repositories = arty.get_repositories()
    config_repositories = sorted([r['key'] for r in conf.get_repositories()])

    for r in actual_repositories:
        if r not in config_repositories:
            log.warn("{0} wasn't found in configuration file".format(r))
            # arty.delete_repository(r)


@click.group()
def cli():
    pass


@cli.command()
@click.option('--url', required=True, type=str,
              help="Artifactory server URL.")
@click.option('--username', required=True, type=str,
              help="Artifactory admin username.")
@click.option('--password', required=True, type=str,
              help="Artifactory admin password.")
@click.option('--config-file', required=True,
              type=click.Path(exists=True, readable=True),
              help="Path to jimbo configuration file.")
def run(url, username, password, config_file):
    _run(url, username, password, config_file)


def setup_logging():
    logging_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(stream=sys.stdout,
                        level=logging.DEBUG,
                        format=logging_format)
    logging.getLogger("requests").setLevel(logging.ERROR)
    logging.getLogger("urllib3").setLevel(logging.ERROR)


def main():
    setup_logging()
    cli()


if __name__ == '__main__':
    main()
