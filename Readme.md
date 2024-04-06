# etcd Command Line Interface (CLI)

This is a Python-based command line interface (CLI) for interacting with etcd, a distributed key-value store. The CLI provides functionalities for checking connection, listing keys with a prefix, putting key-value pairs, getting values for keys, and deleting keys from etcd.

## Installation

**Clone the repository:** 
    ```bash
    git clone https://github.com/deepakk-parmaar/etcd-cli.git
    cd etcd-cli
    ```

## Usage

The CLI supports the following commands:

### `check`

Check the connection to the etcd server.

```bash
python cli.py check
```

### `list <prefix>`

List all keys in etcd with a specified prefix.

```bash
python cli.py list <prefix>
```

### `put <key> <value>`

Put a key-value pair into etcd.

```bash
python cli.py put <key> <value>
```

### `get <key>`

Get the value for a key from etcd.

```bash
python cli.py get <key>
```

### `delete <key>`

Delete a key from etcd.

```bash
python cli.py delete <key>
```

## Configuration

You can configure the host and port of the etcd server by modifying the `cli.py` file directly:

```python
etcd_client = etcd3.client(host='127.0.0.1', port=2379)
```

Modify the `host` and `port` arguments according to your etcd server configuration.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.