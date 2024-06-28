''' All tests related to the list-urls command '''

from unittest.mock import patch
from click.testing import CliRunner

from app.cmd.login import login
from app.tests.dependencies import MockResponse

def test_login():
    ''' Performs all login tests '''
    #pylint: disable=no-value-for-parameter
    test_login_missing_username()
    test_login_short_username()
    test_login_long_username()

    test_login_missing_password()
    test_login_short_password()
    test_login_long_password()

    test_login_user_does_not_exist()
    test_login_incorrect_password()
    test_login_success()
    #pylint: enable=no-value-for-parameter

def test_login_missing_username():
    ''' Tests a login attempt missing the username '''
    runner = CliRunner()
    result = runner.invoke(login, ['-p', 'password'])

    assert result.exit_code == 2

    error = "Usage: login [OPTIONS]\n" \
        "Try 'login --help' for help.\n\n" \
        "Error: Missing option '-u' / '--username'.\n"

    assert result.output == error

def test_login_short_username():
    ''' Tests a login attempt with too short of a username '''
    runner = CliRunner()
    result = runner.invoke(login, ['-u', 't', '-p', 'password'])

    assert result.exit_code == 0

    error = "Validation error: username: 'String should have at least 4 characters'\n"
    assert result.output == error

def test_login_long_username():
    ''' Tests a login attempt with too long of a username '''
    runner = CliRunner()
    result = runner.invoke(login, ['-u', 'testingtoolongusername', '-p', 'password'])

    assert result.exit_code == 0

    error = "Validation error: username: 'String should have at most 16 characters'\n"
    assert result.output == error

def test_login_missing_password():
    ''' Tests a login attempt missing the password '''
    runner = CliRunner()
    result = runner.invoke(login, ['-u', 'test'])

    assert result.exit_code == 2

    error = "Usage: login [OPTIONS]\n" \
        "Try 'login --help' for help.\n\n" \
        "Error: Missing option '-p' / '--password'.\n"

    assert result.output == error

def test_login_short_password():
    ''' Tests a login attempt with too short of a password'''
    runner = CliRunner()
    result = runner.invoke(login, ['-u', 'test', '-p', 'p'])

    assert result.exit_code == 0

    error = "Validation error: password: 'String should have at least 8 characters'\n"
    assert result.output == error

def test_login_long_password():
    ''' Tests a login attempt with too long of a password '''
    runner = CliRunner()
    result = runner.invoke(login, ['-u', 'test', 
                                   '-p', 'passwordiswaytoolonglikeseriouslywhyisitsolong'])

    assert result.exit_code == 0

    error = "Validation error: password: 'String should have at most 32 characters'\n"
    assert result.output == error

@patch('app.cmd.login.requests.post')
def test_login_user_does_not_exist(mock_post):
    ''' Tests a successful login '''
    data = {'detail': 'User does not exist.'}
    mock_post.return_value = MockResponse(status_code=422, json_data=data)

    url='https://shrtnurl.com/token'
    header = {'content-type': 'application/x-www-form-urlencoded'}
    payload = {'username': 'test', 'password': 'passwords', 'grant_type': 'password'}

    runner = CliRunner()
    result = runner.invoke(login, ['-u', 'test', '-p', 'passwords'])

    assert result.output == 'API error: User does not exist.\n'
    assert result.exit_code == 0
    mock_post.assert_called_once_with(url, headers=header, data=payload, timeout=1)

@patch('app.cmd.login.requests.post')
def test_login_incorrect_password(mock_post):
    ''' Tests a successful login '''
    data = {'detail': 'Incorrect Password'}
    mock_post.return_value = MockResponse(status_code=403, json_data=data)

    url='https://shrtnurl.com/token'
    header = {'content-type': 'application/x-www-form-urlencoded'}
    payload = {'username': 'test', 'password': 'passwords', 'grant_type': 'password'}

    runner = CliRunner()
    result = runner.invoke(login, ['-u', 'test', '-p', 'passwords'])

    assert result.output == 'API error: Incorrect Password\n'
    assert result.exit_code == 0
    mock_post.assert_called_once_with(url, headers=header, data=payload, timeout=1)

@patch('app.cmd.login.set_key')
@patch('app.cmd.login.requests.post')
def test_login_success(mock_post, mock_save):
    ''' Tests a successful login '''
    data = {'access_token': 'faketoken', 'token_type': 'bearer'}
    mock_post.return_value = MockResponse(status_code=200, json_data=data)
    mock_save.return_value = (None, '', '')

    url='https://shrtnurl.com/token'
    header = {'content-type': 'application/x-www-form-urlencoded'}
    payload = {'username': 'test', 'password': 'password', 'grant_type': 'password'}

    runner = CliRunner()
    result = runner.invoke(login, ['-u', 'test', '-p', 'password'])

    assert result.output == 'Successfully retrieved token.\n'
    assert result.exit_code == 0
    mock_post.assert_called_once_with(url, headers=header, data=payload, timeout=1)
