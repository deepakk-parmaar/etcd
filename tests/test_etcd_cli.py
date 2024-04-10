import pytest
from click.testing import CliRunner
from unittest.mock import MagicMock
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from etcd_cli import cli


@pytest.fixture
def runner():
    return CliRunner()

def test_check_success(runner, mocker):
    # Mock etcd3.client to simulate a successful connection
    mock_put = MagicMock(return_value=True)  # Simulate successful put operation
    mock_delete = MagicMock(return_value=True)  # Simulate successful delete operation
    mock_client = MagicMock()
    mock_client.put = mock_put
    mock_client.delete = mock_delete

    # Patch get_etcd_client to return the mock_client
    mocker.patch('etcd_cli.get_etcd_client', return_value=mock_client)

    result = runner.invoke(cli, ['check'])
    assert result.exit_code == 0
    assert 'Connection to etcd cluster successful.' in result.output

def test_check_failure(runner, mocker):
    # Mock etcd3.client to raise an exception
    mock_client = MagicMock(side_effect=Exception("Connection failed"))

    # Patch get_etcd_client to return the mock_client
    mocker.patch('etcd_cli.get_etcd_client', return_value=mock_client)

    result = runner.invoke(cli, ['check'])
    assert result.exit_code == 0
    assert 'Error connecting to etcd cluster' in result.output

def test_list_success(runner, mocker):
    # Mock etcd3.client and its get_prefix method to return a test response
    mock_get_prefix = MagicMock(return_value=[('test_key', 'test_value')])
    mock_client = MagicMock()
    mock_client.get_prefix = mock_get_prefix

    # Patch get_etcd_client to return the mock_client
    mocker.patch('etcd_cli.get_etcd_client', return_value=mock_client)

    result = runner.invoke(cli, ['list', 'prefix'])
    assert result.exit_code == 0
    assert 'test_key' in result.output

def test_put_success(runner, mocker):
    # Mock etcd3.client and its put method to simulate successful put operation
    mock_put = mocker.MagicMock(return_value=True)  # Simulate successful put operation
    mock_client = mocker.patch('etcd_cli.get_etcd_client')  # Patch get_etcd_client
    mock_client.return_value.put = mock_put

    result = runner.invoke(cli, ['put', 'test_key', 'test_value'])
    assert result.exit_code == 0
    assert 'Put: key=test_key, value=test_value' in result.output

def test_put_failure(runner, mocker):
    # Mock etcd3.client to raise an exception
    mock_put = mocker.MagicMock(side_effect=Exception("Connection failed"))  # Simulate exception
    mock_client = mocker.patch('etcd_cli.get_etcd_client')  # Patch get_etcd_client
    mock_client.return_value.put = mock_put

    result = runner.invoke(cli, ['put', 'test_key', 'test_value'])
    assert result.exit_code != 0
    assert 'Error while putting the key-value pair' in result.output



def test_get_success(runner, mocker):
    # Mock etcd3.client and its get method to simulate successful get operation
    mock_get = mocker.MagicMock(return_value=('test_value', None))  # Simulate successful get operation
    mock_client = mocker.patch('etcd_cli.get_etcd_client')  # Patch get_etcd_client
    mock_client.return_value.get = mock_get

    result = runner.invoke(cli, ['get', 'test_key'])
    assert result.exit_code == 0
    assert 'Value for key test_key: test_value' in result.output



def test_get_failure(runner, mocker):
    # Mock etcd3.client to raise an exception
    mock_get = mocker.MagicMock(side_effect=Exception("Connection failed"))  # Simulate exception
    mock_client = mocker.patch('etcd_cli.get_etcd_client')  # Patch get_etcd_client
    mock_client.return_value.get = mock_get

    result = runner.invoke(cli, ['get', 'test_key'])
    assert result.exit_code != 0
    assert 'Error while getting the value for key test_key' in result.output



def test_delete_success(runner, mocker):
    # Mock etcd3.client and its delete method to simulate successful deletion
    mock_delete = mocker.MagicMock(return_value=True)  # Simulate successful deletion
    mock_client = mocker.patch('etcd_cli.get_etcd_client')  # Patch get_etcd_client
    mock_client.return_value.delete = mock_delete

    result = runner.invoke(cli, ['delete', 'test_key'])
    assert result.exit_code == 0
    assert 'Deleted key: test_key' in result.output



def test_delete_failure(runner, mocker):
    # Mock etcd3.client to raise an exception
    mock_delete = mocker.MagicMock(side_effect=Exception("Connection failed"))  # Simulate exception
    mock_client = mocker.patch('etcd_cli.get_etcd_client')  # Patch get_etcd_client
    mock_client.return_value.delete = mock_delete

    result = runner.invoke(cli, ['delete', 'test_key'])
    assert result.exit_code != 0
    assert 'Error while deleting key test_key' in result.output

def test_get_all_success(runner, mocker):
    # Define a response generator with some key-value pairs
    response_generator = [(b'key1', b'value1'), (b'key2', b'value2')]

    # Mock etcd_client.get_all() to return the predefined response generator
    mock_get_all = mocker.MagicMock(return_value=response_generator)
    mock_client = mocker.patch('etcd_cli.get_etcd_client')  # Patch get_etcd_client
    mock_client.return_value.get_all = mock_get_all

    result = runner.invoke(cli, ['get_all'])
    assert result.exit_code == 0
    assert 'key1: value1' in result.output
    assert 'key2: value2' in result.output

def test_get_all_failure(runner, mocker):
    # Mock etcd_client.get_all() to raise an exception
    mock_get_all = mocker.MagicMock(side_effect=etcd3.exceptions.Etcd3Exception("Error message"))
    mock_client = mocker.patch('etcd_cli.get_etcd_client')  # Patch get_etcd_client
    mock_client.return_value.get_all = mock_get_all

    result = runner.invoke(cli, ['get_all'])
    assert result.exit_code != 0
    assert 'Error while getting all key-value pairs' in result.output

