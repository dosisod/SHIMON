# SHIMON

Secure Human Interactions Made Over Networks

A simplistic messaging app using python3 and flask

## Installing

```
$ git clone https://github.com/dosisod/SHIMON.git
$ cd SHIMON
$ pip3 install -r requirements.txt
```

Additional requirements:
* Command-line version of gpg (check with `whereis gpg`)
* Access to localhost port 1717

## Development

For developers, run the following:

```
$ tsc --build tsconfig.json
```

This will allow for use of compiled TS files after enabling:

`ACCOUNT > SETTINGS > ENABLE DEVELOPER MODE > USE FRESH JS`

## Running

Run with `python3 main.py`

Got to `http://0.0.0.0:1717` in a web browser

Debug cache password is `123` (this can be changed after unlocking)

## Note

This web app is under development, many features have yet to be implemented

## The Future

In the future I plan to:
* Add networking capabilities
* Compile to working webapp/apk