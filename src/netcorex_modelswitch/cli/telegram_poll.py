from __future__ import annotations

import argparse

from netcorex_modelswitch.channels.telegram.runtime import TelegramRuntime


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Poll Telegram updates once for NetCoreX ModelSwitch")
    parser.add_argument("--offset", type=int, default=None, help="Optional Telegram update offset")
    parser.add_argument("--timeout", type=int, default=1, help="Long polling timeout in seconds")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    runtime = TelegramRuntime()
    next_offset = runtime.poll_once(offset=args.offset, timeout=args.timeout)
    print(next_offset if next_offset is not None else "NO_UPDATES")


if __name__ == "__main__":
    main()
