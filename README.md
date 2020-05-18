# SHIMON

![](https://github.com/dosisod/SHIMON/workflows/tests/badge.svg) ![GitHub](https://img.shields.io/github/license/dosisod/SHIMON) [![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Secure Human Interactions Made Over Networks

A simplistic messaging app using python3 and flask

## Installing

```
$ git clone https://github.com/dosisod/SHIMON.git
$ cd SHIMON
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip3 install -r requirements.txt
```

Additional requirements:
* Command-line version of gpg (check with `whereis gpg`)
* Access to localhost port 1717

## Running

Run with `python3 main.py`

Got to `http://localhost:1717` in a web browser

Debug cache password is `123` (this can be changed after unlocking)

## Developers

### Setup

Before developing, make sure you have installed `typescript`, `sass`, and `minify`:

```
$ npm install -g typescript
$ npm install -g minify
$ npm install -g sass
```

You may need to run the above commands as `sudo`.

### Building

Build TS files using:

```
$ tsc --build tsconfig.json
```

To use the emitted JS files over `bundle.js`, enable:

`ACCOUNT > SETTINGS > ENABLE DEVELOPER MODE > USE FRESH JS`

To copy and bundle JS and CSS files, run:

```
$ python3 min.py
```

Enable use of compiled CSS with:

`ACCOUNT > SETTINGS > ENABLE DEVELOPER MODE > USE FRESH CSS`

### Testing

Install testing requirements:

```
$ pip3 install -r test-requirements.txt
```

Run unit tests with:

```
$ pytest
```

Run type checker with:

```
$ mypy -p SHIMON
```

Run bandit security audit with:

```
$ bandit -r SHIMON
```

## Note

This web app is under development, many features have yet to be implemented

## The Future

In the future I plan to:
* Add networking capabilities
* Compile to working webapp/apk