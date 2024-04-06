import pytest
from click.testing import CliRunner
from etcd_cli import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_check_success(runner, mocker):
    # Mock etcd3.client so that it doesn't actually connect to an etcd server
    mock_client = mocker.patch('etcd3.client')
    mock_client.return_value.put.return_value = True

    result = runner.invoke(cli, ['check'])
    assert result.exit_code == 0
    assert 'Connection to etcd server successful.' in result.output


def test_check_failure(runner, mocker):
    # Mock etcd3.client to raise an exception
    mock_client = mocker.patch('etcd3.client')
    mock_client.side_effect = Exception("Connection failed")

    result = runner.invoke(cli, ['check'])
    assert result.exit_code != 0
    assert 'Error connecting to etcd server' in result.output


def test_list_success(runner, mocker):
    # Mock etcd3.client and its get_prefix method to return a test response
    mock_client = mocker.patch('etcd3.client')
    mock_get_prefix = mocker.MagicMock()
    mock_get_prefix.return_value = [('test_key', 'test_value')]
    mock_client.return_value.get_prefix = mock_get_prefix

    result = runner.invoke(cli, ['list', 'prefix'])
    assert result.exit_code == 0
    assert 'test_key' in result.output


def test_list_failure(runner, mocker):
    # Mock etcd3.client to raise an exception
    mock_client = mocker.patch('etcd3.client')
    mock_client.side_effect = Exception("Connection failed")

    result = runner.invoke(cli, ['list', 'prefix'])
    assert result.exit_code != 0
    assert 'Error while listing keys' in result.output


def test_put_success(runner, mocker):
    # Mock etcd3.client and its put method to simulate successful put operation
    mock_client = mocker.patch('etcd3.client')
    mock_client.return_value.put.return_value = True

    result = runner.invoke(cli, ['put', 'test_key', 'test_value'])
    assert result.exit_code == 0
    assert 'Put: key=test_key, value=test_value' in result.output


def test_put_failure(runner, mocker):
    # Mock etcd3.client to raise an exception
    mock_client = mocker.patch('etcd3.client')
    mock_client.side_effect = Exception("Connection failed")

    result = runner.invoke(cli, ['put', 'test_key', 'test_value'])
    assert result.exit_code != 0
    assert 'Error while putting the key-value pair' in result.output


def test_get_success(runner, mocker):
    # Mock etcd3.client and its get method to simulate successful get operation
    mock_client = mocker.patch('etcd3.client')
    mock_client.return_value.get.return_value = ('test_value', None)

    result = runner.invoke(cli, ['get', 'test_key'])
    assert result.exit_code == 0
    assert 'Value for key test_key: test_value' in result.output


def test_get_failure(runner, mocker):
    # Mock etcd3.client to raise an exception
    mock_client = mocker.patch('etcd3.client')
    mock_client.side_effect = Exception("Connection failed")

    result = runner.invoke(cli, ['get', 'test_key'])
    assert result.exit_code != 0
    assert 'Error while getting the value for key test_key' in result.output


def test_delete_success(runner, mocker):
    # Mock etcd3.client and its delete method to simulate successful deletion
    mock_client = mocker.patch('etcd3.client')
    mock_client.return_value.delete.return_value = True

    result = runner.invoke(cli, ['delete', 'test_key'])
    assert result.exit_code == 0
    assert 'Deleted key: test_key' in result.output


def test_delete_failure(runner, mocker):
    # Mock etcd3.client to raise an exception
    mock_client = mocker.patch('etcd3.client')
    mock_client.side_effect = Exception("Connection failed")

    result = runner.invoke(cli, ['delete', 'test_key'])
    assert result.exit_code != 0
    assert 'Error while deleting key test_key' in result.output
