# etcd Command Line Interface (CLI)

This is a Python-based command line interface (CLI) for interacting with etcd, a distributed key-value store. The CLI provides functionalities for checking connection, getting all the key-value pairs, listing keys with a prefix, putting key-value pairs, getting values for keys, and deleting keys from etcd.

## Installation

**Clone the repository:**
`bash
    git clone https://github.com/deepakk-parmaar/etcd-cli.git
    cd etcd-cli
    `

## Prerequisites

The CLI requires the following Python packages:

- `etcd3` for interacting with etcd
- `click` for building the CLI

You can install the required packages using the following command:

```bash
pip install -r etcd3 click
```

## Docker Image

The Nodes have to run as a Docker container. To build the Docker image, run the following command in the root directory of the project:

```bash
docker-compose up build
```

## Usage

The CLI supports the following commands:

### `check`

Check the connection to the etcd server.

```bash
python etcd_cli.py check
```

### `list <prefix>`

List all keys in etcd with a specified prefix.

```bash
python etcd_cli.py list <prefix>
```

### `put <key> <value>`

Put a key-value pair into etcd.

```bash
python etcd_cli.py put <key> <value>
```

### `get <key>`

Get the value for a key from etcd.

```bash
python etcd_cli.py get <key>
```

### `delete <key>`

Delete a key from etcd.

```bash
python etcd_cli.py delete <key>
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
