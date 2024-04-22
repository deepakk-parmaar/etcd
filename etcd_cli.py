import click
import etcd3

ports = ['2369', '2370', '2371']

@click.group()
def cli():
    """Command line interface for etcd"""
    pass

def get_etcd_client():
    while True:
        for port in ports:
            try:
                etcd_client = etcd3.client(port=int(port))
                # etcd_client.put('test_key', 'test_value')
                # # click.secho('Connected to port {}'.format(port), fg='green')
                # etcd_client.delete('test_key')
                return etcd_client
            except Exception as e:
                click.secho('Error connecting to port={}: {}'.format(port, e), fg='red')
                click.echo('Trying next port...')
                continue

@cli.command()
def check():
    try:
        etcd_client = get_etcd_client()
        etcd_client.put('test_key', 'test_value')
        click.secho('Connection to etcd cluster successful.', fg='green')
        etcd_client.delete('test_key')
        status = etcd_client.status()
        # click.echo('Raft term: {}'.format(status.raft_term))
        click.echo('Leader ID: {}'.format(status.leader))
        # click.echo('Raft index: {}'.format(status.raft_index))
        # click.echo('Version: {}'.format(status.version))
        # click.echo('db size: {}'.format(status.db_size))

        return True
    except Exception as e:
        click.secho('Error connecting to etcd cluster: {}'.format(e), fg='red')
        return False

@cli.command()
@click.argument('prefix')
def list(prefix):
    """List all keys in etcd with prefix"""
    etcd_client = get_etcd_client()
    try:
        response = etcd_client.get_prefix(prefix)
        for key, value in response:
            click.echo(key.decode())
            
    except etcd3.exceptions.Etcd3Exception as e:
        click.secho('Error while listing keys: {}'.format(e), fg='red')

@cli.command()
@click.argument('key')
@click.argument('value')
def put(key, value):
    """Put a key-value pair into etcd"""
    etcd_client = get_etcd_client()
    try:
        etcd_client.put(key, value)
        click.secho('Put: key={}, value={}'.format(key, value), fg='green')
    except etcd3.exceptions.Etcd3Exception as e:
        click.secho('Error while putting the key-value pair: {}'.format(e), fg='red')

@cli.command()
@click.argument('key')
def get(key):
    """Get the value for a key from etcd"""
    etcd_client = get_etcd_client()
    try:
        value, _ = etcd_client.get(key)
        if value is not None:
            click.secho('Value for key {}: {}'.format(key, value.decode()), fg='green')
        else:
            click.secho('Key {} not found'.format(key), fg='yellow')
    except etcd3.exceptions.Etcd3Exception as e:
        click.secho('Error while getting the value for key {}: {}'.format(key, e), fg='red')

@cli.command()
@click.argument('key')
def delete(key):
    """Delete a key from etcd"""
    etcd_client = get_etcd_client()
    try:
        etcd_client.delete(key)
        click.secho('Deleted key: {}'.format(key), fg='green')
    except etcd3.exceptions.KeyNotFoundError:
        click.secho('Key {} not found'.format(key), fg='yellow')
    except etcd3.exceptions.Etcd3Exception as e:
        click.secho('Error while deleting key {}: {}'.format(key, e), fg='red')

@cli.command()
def get_all():
    """Get all key-value pairs from etcd"""
    etcd_client = get_etcd_client()
    try:
        response_generator = etcd_client.get_all()
        for value, metadata in response_generator:
            key_str = metadata.key.decode()
            value_str = value.decode()
            click.echo('{}: {}'.format(key_str, value_str))
    except etcd3.exceptions.Etcd3Exception as e:
        click.secho('Error while getting all key-value pairs: {}'.format(e), fg='red')

if __name__ == '__main__':
    cli()
