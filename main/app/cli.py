import click
from flask import current_app
from app import population
import logging

logger = logging.getLogger(__name__)


@click.command("populate-db")
def populate_db():
    """uses population script to populate db"""
    click.echo("populating db...")
    logger.debug("populating db...")

    population.add_users()
    population.add_classes()
    population.add_userclasses()
    population.add_lessons()

    click.echo("done populating")
    logger.debug("done populating")
