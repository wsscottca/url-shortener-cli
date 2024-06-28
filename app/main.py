''' Main module of CLI for API Interaction '''

import click
from dotenv import find_dotenv, load_dotenv

from app.cmd.list import list_urls
from app.cmd.login import login
from app.cmd.shorten import shorten
from app.cmd.lookup import lookup
from app.tests.perform_tests import tests

load_dotenv(find_dotenv())

@click.group()
def cmds():
    ''' CLI commands group '''

cmds.add_command(shorten)
cmds.add_command(login)
cmds.add_command(list_urls)
cmds.add_command(lookup)

def cli():
    ''' Start CLI '''
    tests()
    cmds()
