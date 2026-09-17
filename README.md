# Mini URL Shortener

A small command-line URL shortener built using Python 3 and the
standard library.

The project takes a long HTTP/HTTPS URL and generates a shorter
code that can later be used to retrieve the original URL.

This implementation follows the first-year CLI track of the
assignment and focuses on simple persistent storage, input
validation, and clean command-line usage.

---

## Features

### Required Features

- Shorten a long URL into a unique short code
- Resolve a short code back to the original URL
- List all stored URL mappings
- Persistent storage using a JSON file
- HTTP and HTTPS URL validation
- Duplicate URL detection
- Handling of missing short codes
- Handling of duplicate custom aliases

### Additional Features

- Custom aliases using `--alias`
- Resolution/click counter
- `stats` command for basic usage statistics
- `--open` option to open the original URL in the browser
- Automated tests using Python's built-in `unittest` module

---

## Technologies Used

- **Python 3**
- **JSON** for persistent data storage
- **argparse** for command-line argument parsing
- **secrets** for generating random short codes
- **unittest** for automated testing
- Python standard library only

No external packages or URL-shortening APIs are used.

---

## Requirements

- Python 3.9 or newer is recommended
- No third-party libraries are required

You can check your Python version with:

```bash
python --version
```

---

## Installation / Setup

Clone or download the repository and open the project folder
in a terminal.

The project structure is:

```text
mini-url-shortener/
│
├── main.py
├── test_main.py
├── README.md
├── .gitignore
└── urls.json
```

The `urls.json` file is used to store the shortened URLs.

If the file does not exist, the program creates it when the
first URL is shortened.

---

## Running the Program

To see all available commands:

```bash
python main.py --help
```

You can also see help for an individual command:

```bash
python main.py shorten --help
python main.py resolve --help
python main.py list --help
python main.py stats --help
```

---

## 1. Shorten a URL

Use the `shorten` command followed by a long URL.

```bash
python main.py shorten "https://www.google.com"
```

Example output:

```text
URL shortened successfully!
Code: hnyA5c
Short URL: http://short.local/hnyA5c
```

The generated code is six characters long and contains random
letters and numbers.

The mapping is immediately saved to `urls.json`.

### Duplicate URL

If the same URL is shortened again, the program does not create
another mapping.

```bash
python main.py shorten "https://www.google.com"
```

Example:

```text
Already shortened: hnyA5c
Short URL: http://short.local/hnyA5c
```

---

## 2. Use a Custom Alias

A custom alias can be provided using `--alias`.

```bash
python main.py shorten "https://github.com/" --alias github
```

Example output:

```text
URL shortened successfully!
Code: github
Short URL: http://short.local/github
```

Aliases can contain:

- Letters
- Numbers
- `_`
- `-`

They must be between 3 and 32 characters long.

An alias cannot be used if it already exists.

Example:

```text
Alias 'github' is already in use.
```

---

## 3. Resolve a Short Code

Use the `resolve` command to find the original URL.

```bash
python main.py resolve hnyA5c
```

Example output:

```text
Original URL: https://www.google.com
Resolution count: 1
```

Every successful resolution increases the resolution count
stored for that URL.

### Missing Code

If a code does not exist:

```bash
python main.py resolve abc123
```

The program displays:

```text
Code 'abc123' was not found.
```

The program exits without changing the stored data.

---

## 4. Open the Original URL

The `--open` option can be used with `resolve`.

```bash
python main.py resolve hnyA5c --open
```

This resolves the code and attempts to open the original URL
in the system's default web browser.

---

## 5. List All URLs

The `list` command displays all stored mappings.

```bash
python main.py list
```

Example:

```text
CODE                   CLICKS  CREATED (UTC)               URL
----------------------------------------------------------------------------------------------------
hnyA5c                       1  2026-09-17T12:30:00+00:00 https://www.google.com
github                       0  2026-09-17T12:31:00+00:00 https://github.com/

Total links: 2
```

The list includes:

- Short code
- Number of resolutions
- Creation time
- Original URL

---

## 6. View Statistics

The `stats` command provides a small summary of the stored
data.

```bash
python main.py stats
```

Example:

```text
URL SHORTENER STATS
------------------------------
Total links       : 2
Total resolutions : 4
Most visited code : hnyA5c
Most visited URL  : https://www.google.com
Clicks on it      : 4
```

This makes it possible to see how many links have been created
and how many times they have been resolved.

---

## URL Validation

The program accepts URLs using the HTTP and HTTPS protocols.

Examples of valid URLs:

```text
https://www.google.com
https://github.com/example/project
http://example.com
```

Invalid input is rejected.

For example:

```bash
python main.py shorten "example.com"
```

will produce an error because the URL does not specify
`http://` or `https://`.

URLs containing spaces are also rejected.

---

## Persistent Storage

The shortened URLs are stored in:

```text
urls.json
```

The data is not kept only in memory.

Each saved mapping contains information similar to:

```json
{
  "hnyA5c": {
    "url": "https://www.google.com",
    "created_at": "2026-09-17T12:30:00+00:00",
    "clicks": 4
  }
}
```

This means the mappings remain available even after the
program is closed and started again.

JSON was chosen because it is simple, readable, and available
through Python's standard library.

---

## How Short Codes Work

For automatically generated codes, the program uses Python's
`secrets` module to generate six random characters.

The character set contains:

- Uppercase letters
- Lowercase letters
- Numbers

Before saving a generated code, the program checks that the
code is not already present in the stored data.

Custom aliases are checked in the same way to prevent duplicate
codes.

---

## Error Handling

The program handles several common error cases gracefully.

| Situation | Program behavior |
|---|---|
| Invalid URL | Displays an error message |
| URL contains spaces | Rejects the URL |
| Unsupported protocol | Rejects the URL |
| Duplicate URL | Returns the existing short code |
| Duplicate alias | Displays an error |
| Missing code | Displays a not-found message |
| Empty database | Displays an appropriate message |
| Invalid/corrupted JSON | Displays an error instead of silently continuing |

---

## Testing

The project includes automated tests in:

```text
test_main.py
```

The tests use Python's built-in `unittest` framework.

Run them with:

```bash
python -m unittest test_main.py -v
```

The tests cover:

- Valid URL handling
- Invalid URL handling
- Shortening and resolving URLs
- Duplicate URL handling
- Custom aliases
- Duplicate aliases
- Missing short codes

The tests use a temporary JSON file, so the normal
`urls.json` data is not modified during testing.

---

## Example Workflow

A typical session could look like this:

### Step 1 — Create a short URL

```bash
python main.py shorten "https://github.com/"
```

Output:

```text
URL shortened successfully!
Code: aB92xK
Short URL: http://short.local/aB92xK
```

### Step 2 — Resolve it

```bash
python main.py resolve aB92xK
```

Output:

```text
Original URL: https://github.com/
Resolution count: 1
```

### Step 3 — Check stored links

```bash
python main.py list
```

### Step 4 — Check statistics

```bash
python main.py stats
```

This demonstrates the complete basic workflow of the
application.

---

## Design Decisions

### Why JSON?

JSON keeps the storage simple and easy to inspect while still
providing persistence between program runs.

For a small first-year CLI project, a full database would add
extra setup without being necessary for the required features.

### Why `argparse`?

`argparse` provides a clean way to implement commands such as:

```text
shorten
resolve
list
stats
```

It also automatically provides command-line help.

### Why `secrets`?

The `secrets` module is part of Python's standard library and
is designed for generating random values. It is used here to
create unpredictable short codes.

### Why no external API?

The assignment requires the shortener to work independently.
All shortening and resolving logic is implemented locally.

---

## Note About `short.local`

The displayed short URL looks like:

```text
http://short.local/hnyA5c
```

This is only a representation of the shortened URL for this
CLI project.

It is **not a deployed public website**.

The actual resolving is performed by the Python program:

```bash
python main.py resolve hnyA5c
```

---

## Limitations

This is a local command-line project, so it does not currently
provide:

- A public web server
- A real internet-accessible short URL
- Multiple-user accounts
- Cloud/database storage
- Authentication
- Analytics beyond the local resolution counter

These features could be added in a larger web-based version.

---

## Future Improvements

Possible extensions for a future version include:

- Flask-based web interface
- SQLite or another database
- Expiring links
- More detailed analytics
- REST API
- User accounts
- QR code generation
- Deployment as a public service

These are outside the scope of the current CLI assignment.

---

## Project Goal

The main goal of this project was to build a small but complete
command-line application while practicing:

- Python functions and modules
- File handling
- JSON data storage
- Command-line arguments
- Input validation
- Error handling
- Random code generation
- Automated testing

The implementation intentionally uses only Python's standard
library and keeps the project simple enough to understand and
modify.
python main.py --help
