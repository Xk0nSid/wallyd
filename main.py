#!/usr/bin/env python

import click
import logging
import toml
from sys import exit
from wally import Wally


VERSION = "0.1.0"


def parse_config(f):
    return toml.loads(f.read())


@click.group()
def cli():
    """
    Wally is a wallpaper daemon, that automatically
    changes wallpapers after a set interval of time.
    Wally supports local wallpapers as well as remote
    wallpapers via `Unsplash`.
    """
    pass


@cli.command()
def version():
    """
    Prints version info of Wally.
    """
    click.echo("Wally Server {}".format(VERSION))


@cli.command()
@click.option('--config', type=click.File('r'), default='./wally.toml', help="Server configuration file")
@click.option('--no-restore', is_flag=True, default=False, help="Don't restore previous state.")
def server(config, no_restore):
    """
    Start the wally server
    """

    # Setup logger
    logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] (%(module)8s:L%(lineno)d) : %(message)s',
        datefmt='%Y/%m/%d %H:%M:%S')

    logging.info("Parsing config file {}".format(config.name))
    config = parse_config(config)
    if not config:
        logging.critical("Failed to parse config file")
        exit(1)
    logging.info("Success")

    logging.info("Initializing server")
    Wally(config).run(no_restore)
