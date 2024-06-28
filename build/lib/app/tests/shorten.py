''' Module of all tests for shorten command'''

from unittest.mock import patch
from click.testing import CliRunner

from app.cmd.shorten import shorten
from app.tests.dependencies import MockResponse

def test_shorten():
    ''' Performs all login tests '''
    #pylint: disable=no-value-for-parameter
    test_shorten_missing_url()
    test_shorten_invalid_url()
    test_shorten_long_short_url()
    test_shorten_existing_short_url()
    test_shorten_short_url_successful()
    test_shorten_no_short_url_successful()
    #pylint: enable=no-value-for-parameter

def test_shorten_missing_url():
    ''' Tests a shorten attempt missing the url '''
    runner = CliRunner()
    result = runner.invoke(shorten, ['--short-url', '1234567'])

    assert result.exit_code == 2

    error = "Usage: shorten [OPTIONS]\n" \
        "Try 'shorten --help' for help.\n\n" \
        "Error: Missing option '--url'.\n"

    assert result.output == error

def test_shorten_invalid_url():
    ''' Tests a shorten attempt with an invalid url '''
    runner = CliRunner()
    result = runner.invoke(shorten, ['--url', 'notaurl'])

    assert result.exit_code == 0

    error = "Validation error: url: 'Input should be a valid URL, relative URL without a base'\n"

    assert result.output == error

def test_shorten_long_short_url():
    ''' Tests a shorten attempt with too long of a short url '''
    runner = CliRunner()
    result = runner.invoke(shorten, ['--url', 'https://www.google.com',
                                     '--short-url', 'toolongshorturl'])

    assert result.exit_code == 0

    error = "Validation error: short_url: 'String should have at most 8 characters'\n"
    assert result.output == error

@patch('app.cmd.shorten.requests.post')
def test_shorten_existing_short_url(mock_post):
    ''' Tests a shorten attempt with an existing short url '''
    data = {'detail': 'Short URL already exists, please enter a new short URL.'}
    mock_post.return_value = MockResponse(status_code=422, json_data=data)

    runner = CliRunner()
    result = runner.invoke(shorten, ['--url', 'https://www.google.com',
                                     '--short-url', '587ec2a0'])

    assert result.exit_code == 0

    error = "API error: Short URL already exists, please enter a new short URL.\n"
    assert result.output == error

@patch('app.cmd.shorten.requests.post')
def test_shorten_short_url_successful(mock_post):
    ''' Tests a successful url shorten with a custom short url '''
    data = {'short_url': '1', 'url': 'https://www.google.com/'}
    mock_post.return_value = MockResponse(status_code=201, json_data=data)

    runner = CliRunner()
    result = runner.invoke(shorten, ['--url', 'https://www.google.com/',
                                     '--short-url', '1'])

    assert result.exit_code == 0

    res = "Successfully created short URL.\n" \
            "Short URL: 1\n" \
            "URL: https://www.google.com/\n"

    assert res == result.output

@patch('app.cmd.shorten.requests.post')
def test_shorten_no_short_url_successful(mock_post):
    ''' Tests a successful url shorten without a custom short url '''
    data = {'short_url': '1', 'url': 'https://www.google.com/'}
    mock_post.return_value = MockResponse(status_code=201, json_data=data)

    runner = CliRunner()
    result = runner.invoke(shorten, ['--url', 'https://www.google.com/'])

    assert result.exit_code == 0

    res = "Successfully created short URL.\n" \
            "Short URL: 1\n" \
            "URL: https://www.google.com/\n"

    assert res == result.output
