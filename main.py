#!/usr/bin/env python3

import argparse
import json
import re
import secrets
import string
import sys
import webbrowser
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

DATA_FILE = Path(__file__).with_name("urls.json")
CODE_LENGTH = 6
ALIAS_PATTERN = re.compile(r"^[A-Za-z0-9_-]{3,32}$")


def load_data():
    if not DATA_FILE.exists():
        return {}

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("Database must contain a JSON object.")

        return data

    except (json.JSONDecodeError, OSError, ValueError) as exc:
        print(f"Error reading {DATA_FILE.name}: {exc}", file=sys.stderr)
        sys.exit(1)


def save_data(data):
    temp_file = DATA_FILE.with_suffix(".tmp")

    try:
        with temp_file.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
            file.write("\n")

        temp_file.replace(DATA_FILE)

    except OSError as exc:
        temp_file.unlink(missing_ok=True)
        print(f"Error saving data: {exc}", file=sys.stderr)
        sys.exit(1)


def normalize_url(url):
    url = url.strip()
    parsed = urlparse(url)

    if any(char.isspace() for char in url):
        raise ValueError("URL cannot contain spaces.")

    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("URL must start with http:// or https://.")

    if not parsed.netloc:
        raise ValueError("URL must contain a valid domain.")

    return url


def generate_code(existing_codes):
    alphabet = string.ascii_letters + string.digits

    while True:
        code = "".join(secrets.choice(alphabet) for _ in range(CODE_LENGTH))

        if code not in existing_codes:
            return code


def find_by_url(data, url):
    for code, record in data.items():
        if record["url"] == url:
            return code

    return None


def cmd_shorten(args):
    data = load_data()

    try:
        url = normalize_url(args.url)
    except ValueError as exc:
        print(f"Invalid URL: {exc}")
        return 2

    existing_code = find_by_url(data, url)

    if existing_code:
        print(f"Already shortened: {existing_code}")
        print(f"Short URL: http://short.local/{existing_code}")
        return 0

    if args.alias:
        if not ALIAS_PATTERN.fullmatch(args.alias):
            print(
                "Invalid alias. Use 3-32 letters, numbers, '_' or '-'."
            )
            return 2

        if args.alias in data:
            print(f"Alias '{args.alias}' is already in use.")
            return 2

        code = args.alias

    else:
        code = generate_code(data)

    data[code] = {
        "url": url,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "clicks": 0,
    }

    save_data(data)

    print("URL shortened successfully!")
    print(f"Code: {code}")
    print(f"Short URL: http://short.local/{code}")

    return 0


def cmd_resolve(args):
    data = load_data()
    code = args.code.strip()

    if code not in data:
        print(f"Code '{code}' was not found.")
        return 1

    data[code]["clicks"] = data[code].get("clicks", 0) + 1
    save_data(data)

    url = data[code]["url"]

    print(f"Original URL: {url}")
    print(f"Resolution count: {data[code]['clicks']}")

    if args.open:
        try:
            webbrowser.open(url)
            print("Opening in your default browser...")
        except Exception as exc:
            print(f"Could not open browser: {exc}")
            return 1

    return 0


def cmd_list(_args):
    data = load_data()

    if not data:
        print("No shortened URLs yet.")
        return 0

    print(f"{'CODE':<20} {'CLICKS':>7}  {'CREATED (UTC)':<28} URL")
    print("-" * 100)

    for code, record in data.items():
        created = record.get("created_at", "-")[:25]
        clicks = record.get("clicks", 0)

        print(
            f"{code:<20} {clicks:>7}  "
            f"{created:<28} {record['url']}"
        )

    print(f"\nTotal links: {len(data)}")

    return 0


def cmd_stats(_args):
    data = load_data()

    if not data:
        print("No data available yet.")
        return 0

    code, record = max(
        data.items(),
        key=lambda item: item[1].get("clicks", 0),
    )

    total_clicks = sum(
        record.get("clicks", 0)
        for record in data.values()
    )

    print("URL SHORTENER STATS")
    print("-" * 30)
    print(f"Total links       : {len(data)}")
    print(f"Total resolutions : {total_clicks}")
    print(f"Most visited code : {code}")
    print(f"Most visited URL  : {record['url']}")
    print(f"Clicks on it      : {record.get('clicks', 0)}")

    return 0


def build_parser():
    parser = argparse.ArgumentParser(
        description=(
            "A small persistent URL shortener "
            "using Python's standard library."
        )
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    shorten = subparsers.add_parser(
        "shorten",
        help="Create a short code.",
    )
    shorten.add_argument(
        "url",
        help="Long HTTP(S) URL.",
    )
    shorten.add_argument(
        "--alias",
        help="Optional custom alias.",
    )
    shorten.set_defaults(func=cmd_shorten)

    resolve = subparsers.add_parser(
        "resolve",
        help="Resolve a short code.",
    )
    resolve.add_argument(
        "code",
        help="Short code or custom alias.",
    )
    resolve.add_argument(
        "--open",
        action="store_true",
        help="Open the original URL in your browser.",
    )
    resolve.set_defaults(func=cmd_resolve)

    listing = subparsers.add_parser(
        "list",
        help="List all shortened URLs.",
    )
    listing.set_defaults(func=cmd_list)

    stats = subparsers.add_parser(
        "stats",
        help="Show basic usage statistics.",
    )
    stats.set_defaults(func=cmd_stats)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())