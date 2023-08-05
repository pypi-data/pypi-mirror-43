import argparse

from .zipit import build_app


def setup() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Package up application and dependencies into pep 441 .pyz format.")
    parser.add_argument('src', help="Your application")
    parser.add_argument('-d', '--deps', action='append', help="Your applications dependencies")

    return parser


def main():
    parser = setup()
    args = parser.parse_args()

    build_app(
        src=args.src,
        deps=args.deps
    )
