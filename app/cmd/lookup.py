''' Shorten URL command to access API '''

import click
from pydantic import ValidationError
import requests

from app.model.short_url import ShortUrlModel

@click.command()
@click.option('--short-url', type=str, required=True,
              help='The short url that we are finding the url of')
def lookup(short_url):
    '''
    CLI Command to find the associated URL to the provided short url
    
    Args:
        short_url (str): Short url to look up

    Returns:
        Valid URL associated with the provided short url
    '''

    # Validate the inputs
    try:
        ShortUrlModel(short_url=short_url)
    except ValidationError as e:
        details = e.errors()[0]
        loc = details['loc'][0]
        err = details['msg']
        click.echo(f'Validation error: {loc}: \'{err}\'')
        return

    # Send request and get response
    response = requests.get(f'https://shrtnurl.com/{short_url}',
                              timeout=1)

    # If we're successfully redirected grab the URL
    if response.status_code == 200:
        click.echo(response.url)
        return

    # Get data of response through JSON
    json = response.json()

    # If there is an error from the API, relay the details
    if 'detail' in json:
        click.echo(f'API error: {json['detail']}')
        return
