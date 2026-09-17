# Mini URL Shortener

A small command-line URL shortener built using Python 3 and the
standard library.

The program converts long URLs into short codes and allows those
codes to be resolved back to their original URLs.

Built for the first-year CLI track of the assignment.

---

## Features

### Required

- Shorten URLs using `shorten <url>`
- Resolve URLs using `resolve <code>`
- List all stored mappings
- Persistent storage using `urls.json`
- HTTP/HTTPS URL validation
- Duplicate URL handling
- Missing-code handling

### Additional

- Custom aliases using `--alias`
- Resolution/click counter
- `stats` command
- `--open` option to open the original URL
- Automated tests using `unittest`

---

## Quick Demo

```text
$ python main.py shorten "https://github.com/"
URL shortened successfully!
Code: github
Short URL: http://short.local/github

$ python main.py resolve github
Original URL: https://github.com/
Resolution count: 1
```

> `short.local` is only a representation of the short URL for
> this CLI project. It is not a deployed website.

---

## Assignment Requirements

| Requirement | Implementation |
|---|---|
| Shorten URL | `shorten <url>` |
| Resolve URL | `resolve <code>` |
| List mappings | `list` |
| Persistent storage | `urls.json` |
| Invalid URL handling | URL validation |
| Duplicate URL handling | Existing code is returned |
| Missing code handling | Error message |
| Custom alias | `--alias` |
| Resolution count | Click/resolution counter |
| Automated tests | `test_main.py` |

---

## Requirements

- Python 3.9+ recommended
- No third-party packages required

The project uses only Python's standard library.

---

## Running the Program

Open the project folder in a terminal and run:

```bash
python main.py --help
```

### Shorten a URL

```bash
python main.py shorten "https://www.google.com"
```

Example:

```text
URL shortened successfully!
Code: hnyA5c
Short URL: http://short.local/hnyA5c
```

### Custom Alias

```bash
python main.py shorten "https://github.com/" --alias github
```

### Resolve a Code

```bash
python main.py resolve hnyA5c
```

Example:

```text
Original URL: https://www.google.com
Resolution count: 1
```

### Open the Original URL

```bash
python main.py resolve hnyA5c --open
```

### List All Links

```bash
python main.py list
```

### View Statistics

```bash
python main.py stats
```

---

## Persistent Storage

All mappings are stored in `urls.json`, so the data remains
available even after the program is closed.

Each entry stores:

- Original URL
- Creation time
- Resolution count

JSON was chosen because it is simple, readable, and requires no
external database or package.

---

## URL Validation & Error Handling

The program accepts HTTP and HTTPS URLs and rejects invalid
input such as URLs without a supported protocol or URLs
containing spaces.

It also handles:

- Duplicate URLs
- Duplicate aliases
- Missing short codes
- Empty data
- Invalid or corrupted JSON

---

## Testing

Automated tests are included in `test_main.py`.

Run them with:

```bash
python -m unittest test_main.py -v
```

The tests cover URL validation, shortening, resolving,
duplicates, aliases, and missing codes.

Tests use a temporary JSON file, so the project's normal
`urls.json` is not modified.

---

## Project Structure

```text
mini-url-shortener/
│
├── main.py
├── test_main.py
├── README.md
├── .gitignore
└── urls.json
```

---

## Design

Short codes are six random letters/numbers generated using
Python's `secrets` module. Generated codes are checked against
existing codes before being saved.

The project intentionally keeps the implementation small and
focused on the CLI requirements while adding useful features
such as aliases and usage statistics.

---

## Future Improvements

Possible extensions include:

- Database storage
- Flask/web interface
- REST API
- Expiring links
- More detailed analytics
- User accounts
- Deployment as a public service

These are outside the scope of the current CLI assignment.
