''' Login to API command '''

import click
from dotenv import find_dotenv, set_key
from pydantic import ValidationError
import requests

from app.model.password import PasswordModel
from app.model.username import UsernameModel

@click.command()
@click.option('-u', '--username', required=True, type=str,
              help='Username of user to login (4-16 chars)')
@click.option('-p', '--password', required=True, type=str,
              help='Password of user to login (8-32 chars)')
def login(username, password):
    '''
    CLI Command to login to API and receive a token
    
    Args:
        username (str): Username of account to login to
        password (str): Password of account to login to
    
    Returns:
        Token: JWT Token for the API to know who the user is
    '''
    # Validate the inputs
    try:
        UsernameModel(username=username)
        PasswordModel(password=password)
    except ValidationError as e:
        details = e.errors()[0]
        loc = details['loc'][0]
        err = details['msg']
        click.echo(f'Validation error: {loc}: \'{err}\'')
        return

    # Set headers and payload
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    payload = {'username': username, 'password': password, 'grant_type': 'password'}

    # Send request and get response
    response = requests.post('https://shrtnurl.com/token',
                              headers=headers,
                              data=payload,
                              timeout=1)

    # Get data of response through JSON
    json = response.json()

    # If there is an error from the API, relay the details
    if 'detail' in json:
        click.echo(f'API error: {json['detail']}')
        return

    # If no errors and we got a token, store it as an environment variable
    set_key(dotenv_path=find_dotenv(raise_error_if_not_found=True),
            key_to_set="access_token", value_to_set=json['access_token'])
    click.echo('Successfully retrieved token.')
