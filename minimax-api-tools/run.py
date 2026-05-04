"""MiniMax API Tools - unified entry point."""

import argparse
import importlib
import sys

SCRIPTS = {
    "voice-clone": "scripts.voice_clone",
    "tts": "scripts.tts",
    "voice-manage": "scripts.voice_manage",
}


def main():
    parser = argparse.ArgumentParser(
        prog="minimax-tools",
        description="MiniMax API tools runner",
    )
    parser.add_argument(
        "tool",
        choices=list(SCRIPTS.keys()),
        help="Tool to run",
    )
    args, remaining = parser.parse_known_args()

    mod = importlib.import_module(SCRIPTS[args.tool])
    mod.main(remaining)


if __name__ == "__main__":
    main()
