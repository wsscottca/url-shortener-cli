''' List URL command '''

import os
import click
import requests


@click.command()
@click.option('--admin', is_flag=True, default=False,
              help='Flag to run as administrator.')
def list_urls(admin):
    '''
    CLI Command to list URL pairs from API

    Returns:
        The current url pairs in the API database
    '''
    # Verify the user is attempting an admin function
    if not admin:
        click.echo('Insufficient permissions, please login and use the --admin flag.')
        return

    # Attempt to get the token that verifies they have admin privelages
    token = os.getenv('access_token')

    # If they don't have a token they didn't log in,
    if not token:
        click.echo('Insufficient permissions, please login and use the --admin flag.')
        return

    # Set authorization header
    headers = {"Authorization": f"Bearer {token}"}

    # Send request and get response
    response = requests.get('https://shrtnurl.com/list_urls',
                              headers=headers,
                              timeout=1)

    # Get data of response through JSON
    json = response.json()

    # If there is an error from the API, relay the details
    if 'detail' in json:
        click.echo(f'API error: {json['detail']}')
        return

    if not json:
        click.echo('No url pairs exist.')
        return

    click.echo("ShortUrl -> Url")
    for url_pair in json:
        click.echo(f'{url_pair} -> {json[url_pair]}')
