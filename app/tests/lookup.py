''' All tests related to the list-urls command '''

from unittest.mock import patch
from click.testing import CliRunner

from app.cmd.lookup import lookup
from app.tests.dependencies import MockResponse

def test_lookup():
    ''' Performs all login tests '''
    #pylint: disable=no-value-for-parameter
    test_lookup_missing_short_url_flag()
    test_lookup_missing_short_url()
    test_lookup_long_short_url()
    test_lookup_short_url_does_not_exist()
    test_lookup_successful()
    #pylint: enable=no-value-for-parameter

def test_lookup_missing_short_url_flag():
    ''' Tests a lookup attempt missing the short-url flag '''
    runner = CliRunner()
    result = runner.invoke(lookup)

    assert result.exit_code == 2

    error = "Usage: lookup [OPTIONS]\n" \
            "Try 'lookup --help' for help.\n\n" \
            "Error: Missing option '--short-url'.\n"
    assert result.output == error

def test_lookup_missing_short_url():
    ''' Tests a list attempt missing the short-url '''
    runner = CliRunner()
    result = runner.invoke(lookup, ['--short-url'])

    assert result.exit_code == 2

    error = "Error: Option '--short-url' requires an argument.\n"
    assert result.output == error

def test_lookup_long_short_url():
    ''' Tests a lookup attempt with too long of a short url '''
    runner = CliRunner()
    result = runner.invoke(lookup, ['--short-url', 'toolongshorturl'])

    assert result.exit_code == 0

    error = "Validation error: short_url: 'String should have at most 8 characters'\n"
    assert result.output == error

@patch('app.cmd.lookup.requests.get')
def test_lookup_short_url_does_not_exist(mock_get):
    ''' Tests a list attempt with an invalid permissioned user '''
    data = {'detail': 'Short url does not exist.'}
    mock_get.return_value = MockResponse(status_code=422, json_data=data)

    runner = CliRunner()
    result = runner.invoke(lookup, ['--short-url', '1'])

    assert result.exit_code == 0

    error = "API error: Short url does not exist.\n"
    assert result.output == error

@patch('app.cmd.lookup.requests.get')
def test_lookup_successful(mock_get):
    ''' Tests a list attempt with an invalid permissioned user '''
    data = {}
    url = 'https://www.successfullookup.com/'
    mock_get.return_value = MockResponse(status_code=200, json_data=data, url=url)

    runner = CliRunner()
    result = runner.invoke(lookup, ['--short-url', '1'])

    assert result.exit_code == 0
    assert result.output == url + '\n'
