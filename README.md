# Mini URL Shortener

A small command-line URL shortener built with Python 3
standard library only.

This project implements the required first-year CLI features
and adds a few simple extras.

## Features

### Required

- `shorten <url>` - create a short code
- `resolve <code>` - find the original URL
- `list` - show saved links
- Persistent storage using `urls.json`
- URL validation
- Duplicate URL handling
- Missing-code handling

### Extra

- Custom aliases
- Click/resolution counter
- `stats` command
- Automated tests

## Requirements

Python 3.9+ is recommended.

No third-party packages are required.

## Run

First, open the project folder in a terminal.

Then run:

```bash
python main.py --help