import click
import etcd3


@click.group()
def cli():
    '''Command line interface for etcd'''
    pass


@cli.command()
def check():
    try:
        etcd_client = etcd3.client(host='127.0.0.1', port=2379)
        # Try putting a test key-value pair
        etcd_client.put('test_key', 'test_value')
        print('Connection to etcd server successful.')
        return True
    except Exception as e:
        print('Error connecting to etcd server:', e)
        return False


@cli.command()
@click.argument('prefix')
def list(prefix):
    '''List all keys in etcd with prefix '''
    etcd_client = etcd3.client(host='127.0.0.1', port=2379)
    try:
        # Use get_prefix method to fetch key-value pairs with a prefix
        response = etcd_client.get_prefix(prefix)
        for key, value in response:
            print(key.decode())
    except etcd3.exceptions.Etcd3Exception as e:
        print('Error while listing keys:', e)



@cli.command()
@click.argument('key')
@click.argument('value')
def put(key, value):
    '''Put a key-value pair into etcd'''
    etcd_client = etcd3.client(host='127.0.0.1', port=2379)
    try:
        etcd_client.put(key, value)
        print('Put: key={}, value={}'.format(key, value))
    except etcd3.exceptions.Etcd3Exception as e:
        print('Error while putting the key-value pair:', e)


@cli.command()
@click.argument('key')
def get(key):
    '''Get the value for a key from etcd'''
    etcd_client = etcd3.client(host='127.0.0.1', port=2379)
    try:
        value, _ = etcd_client.get(key)
        if value is not None:
            print('Value for key {}: {}'.format(key, value.decode()))
        else:
            print('Key {} not found'.format(key))
    except etcd3.exceptions.KeyNotFoundError:
        print('Key {} not found'.format(key))
    except etcd3.exceptions.Etcd3Exception as e:
        print('Error while getting the value for key {}: {}'.format(key, e))


@cli.command()
@click.argument('key')
def delete(key):
    '''Delete a key from etcd'''
    etcd_client = etcd3.client(host='127.0.0.1', port=2379)
    try:
        etcd_client.delete(key)
        print('Deleted key:', key)
    except etcd3.exceptions.KeyNotFoundError:
        print('Key {} not found'.format(key))
    except etcd3.exceptions.Etcd3Exception as e:
        print('Error while deleting key {}: {}'.format(key, e))


if __name__ == '__main__':
    cli()