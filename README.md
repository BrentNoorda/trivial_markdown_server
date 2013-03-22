trivial_markdown_server
=======================

Serve (github-flavored) markdown files locally to your browser.

It's just one file. It serves MD files in your local browser. That's all.

## Usage

From the `mdview.py --help` output

    Usage: mdview.py filespec.md [options]

    Options:
      -h, --help            show this help message and exit
      -q, --quiet           do not print messages on every request
      --forever             run server forever, even if browser stops requesting
                            markdown files
      -p PORT, --port=PORT  server port (else will search for an available port)

## Example

To view this README.md file locally:

    python mdview.py README.md

This will open README.md in a new tab of your default browser, and continue running until you close that browser tab.

## Requirements

* python
* [markdown](https://pypi.python.org/pypi/Markdown) - e.g. `pip install markdown`

## Why

I got tired of going to github or the [github markdown previewer](http://tmpvar.com/markdown.html) just to read markdown.

## More?

See this project at [BrentNoorda/trivial_markdown_server](https://github.com/BrentNoorda/trivial_markdown_server)

## Even More?

[A simple test](silly/test.md)