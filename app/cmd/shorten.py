''' Shorten URL command to access API '''

import click
from pydantic import HttpUrl, ValidationError
import requests

from app.model.short_url import ShortUrlModel

@click.command()
@click.option('--url', required=True, type=str,
              help='The URL to direct to.')
@click.option('--short-url', type=str,
              help='The requested short url')
def shorten(url, short_url):
    '''
    CLI Command to shorten URL using API
    
    Args:
        url (str): URL to create short URL for
        short_url (str): Preferred short URL string

    Returns:
        Valid short URL that will redirect to the URL
    '''

    # Validate the inputs
    try:
        HttpUrl(url=url)
        if short_url:
            ShortUrlModel(short_url=short_url)
    except ValidationError as e:
        details = e.errors()[0]
        loc = details['loc']

        if loc == ():
            loc = 'url'
        else:
            loc = loc[0]

        err = details['msg']
        click.echo(f'Validation error: {loc}: \'{err}\'')
        return

    # Set payload
    payload = {'url': url, 'short_url': short_url}

    # Send request and get response
    response = requests.post('https://shrtnurl.com/shorten_url',
                              params=payload,
                              timeout=1)

    # Get data of response through JSON
    json = response.json()

    # If there is an error from the API, relay the details
    if 'detail' in json:
        click.echo(f'API error: {json['detail']}')
        return

    # Otherwise let the user know the action was successful
    click.echo('Successfully created short URL.')
    click.echo(f'Short URL: { json['short_url'] }')
    click.echo(f'URL: { json['url'] }')
