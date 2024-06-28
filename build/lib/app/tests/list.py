''' All tests related to the list-urls command '''

from unittest.mock import patch
from click.testing import CliRunner

from app.cmd.list import list_urls
from app.tests.dependencies import MockResponse

def test_list():
    ''' Performs all login tests '''
    #pylint: disable=no-value-for-parameter
    test_list_urls_no_flag()
    test_list_missing_token()
    test_list_invalid_permissions()
    test_list_empty()
    test_list_populated()
    #pylint: enable=no-value-for-parameter

def test_list_urls_no_flag():
    ''' Tests a list attempt missing the admin flag '''
    runner = CliRunner()
    result = runner.invoke(list_urls)

    assert result.exit_code == 0

    error = "Insufficient permissions, please login and use the --admin flag.\n"
    assert result.output == error

@patch('app.cmd.list.os.getenv')
def test_list_missing_token(mock_get_token):
    ''' Tests a list attempt missing a token '''
    mock_get_token.return_value = None

    runner = CliRunner()
    result = runner.invoke(list_urls, ['--admin'])

    assert result.exit_code == 0

    error = "Insufficient permissions, please login and use the --admin flag.\n"
    assert result.output == error

@patch('app.cmd.list.os.getenv')
@patch('app.cmd.list.requests.get')
def test_list_invalid_permissions(mock_get, mock_get_token):
    ''' Tests a list attempt with an invalid permissioned user '''
    mock_get_token.return_value = 'faketoken'
    data = {'detail': 'You lack the appropriate permissions to access this route.'}
    mock_get.return_value = MockResponse(status_code=401, json_data=data)

    runner = CliRunner()
    result = runner.invoke(list_urls, ['--admin'])

    assert result.exit_code == 0

    error = "API error: You lack the appropriate permissions to access this route.\n"
    assert result.output == error

@patch('app.cmd.list.os.getenv')
@patch('app.cmd.list.requests.get')
def test_list_empty(mock_get, mock_get_token):
    ''' Tests a successful url shorten without a custom short url '''
    mock_get_token.return_value = 'faketoken'
    data = {}
    mock_get.return_value = MockResponse(status_code=200, json_data=data)

    runner = CliRunner()
    result = runner.invoke(list_urls, ['--admin'])

    assert result.exit_code == 0

    res = "No url pairs exist.\n"
    assert res == result.output

@patch('app.cmd.list.os.getenv')
@patch('app.cmd.list.requests.get')
def test_list_populated(mock_get, mock_get_token):
    ''' Tests a successful url shorten without a custom short url '''
    mock_get_token.return_value = 'faketoken'
    data = {'1': 'url1', '2': 'url2'}
    mock_get.return_value = MockResponse(status_code=200, json_data=data)

    runner = CliRunner()
    result = runner.invoke(list_urls, ['--admin'])

    assert result.exit_code == 0

    res = 'ShortUrl -> Url\n' \
            '1 -> url1\n' \
            '2 -> url2\n'
    
    assert res == result.output
