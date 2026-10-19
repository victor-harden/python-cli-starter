# python-cli-starter

A small CLI skeleton with the pieces every real tool needs: subcommands,
environment-aware configuration, structured logging, predictable exit codes and
tests that exercise the CLI the same way a user would.

## Features

- `argparse` subcommands (`greet`, `config`, `version`).
- Configuration from `--config`, then environment variables, then defaults.
- `--verbose` logging to stderr, normal output to stdout (pipe-friendly).
- Exit codes: `0` success, `1` runtime error, `2` usage error.
- Tests call `main()` and assert stdout, stderr and exit codes.

## Installation

```bash
git clone https://github.com/victor-harden/python-cli-starter.git
cd python-cli-starter
```

## Usage

```bash
python3 cli.py greet --name Victor
python3 cli.py greet --name Victor --shout
python3 cli.py config --show
APP_GREETING=Hola python3 cli.py greet
python3 cli.py version
```

Configuration precedence: `--config file.toml` > `APP_*` environment variables >
built-in defaults.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## License

MIT — see [LICENSE](LICENSE).
