#!/usr/bin/env python3
"""CLI starter with config, logging and subcommands."""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path

APP_NAME = "python-cli-starter"
VERSION = "1.0.0"
DEFAULTS = {"greeting": "Hello", "repeat": 1, "log_level": "warning"}


def load_config(path: Path | None) -> dict:
    """Merge defaults, environment variables and an optional JSON config file."""
    config = dict(DEFAULTS)
    env_map = {"APP_GREETING": "greeting", "APP_REPEAT": "repeat", "APP_LOG_LEVEL": "log_level"}
    for env_key, key in env_map.items():
        if env_key in os.environ:
            config[key] = os.environ[env_key]
    if path is not None:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("config must be a JSON object")
        config.update(data)
    config["repeat"] = int(config["repeat"])
    return config


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog=APP_NAME, description="CLI starter")
    parser.add_argument("--config", type=Path, help="JSON config file")
    parser.add_argument("--verbose", action="store_true", help="debug logging")
    sub = parser.add_subparsers(dest="command", required=True)

    greet = sub.add_parser("greet", help="print a greeting")
    greet.add_argument("--name", default="world")
    greet.add_argument("--shout", action="store_true")

    config = sub.add_parser("config", help="inspect configuration")
    config.add_argument("--show", action="store_true")

    sub.add_parser("version", help="print the version")
    return parser


def configure_logging(verbose: bool, config: dict) -> None:
    level = logging.DEBUG if verbose else getattr(
        logging, str(config.get("log_level", "warning")).upper(), logging.WARNING)
    logging.basicConfig(level=level, format="%(levelname)s %(message)s", stream=sys.stderr)


def cmd_greet(args, config) -> int:
    greeting = f"{config['greeting']}, {args.name}"
    if args.shout:
        greeting = greeting.upper() + "!"
    for _ in range(config["repeat"]):
        print(greeting)
    logging.debug("greeted %s %d time(s)", args.name, config["repeat"])
    return 0


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        config = load_config(args.config)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"config error: {exc}", file=sys.stderr)
        return 1
    configure_logging(args.verbose, config)

    if args.command == "greet":
        return cmd_greet(args, config)
    if args.command == "config":
        print(json.dumps(config, indent=2))
        return 0
    if args.command == "version":
        print(f"{APP_NAME} {VERSION}")
        return 0
    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
