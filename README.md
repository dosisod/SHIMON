# SHIMON

Secure Human Interactions Made Over Networks

A simplistic messaging app using python3 and flask

## Installing

```
git clone https://github.com/dosisod/SHIMON.git
cd SHIMON
pip3 install -r requirements.txt
```

Additional requirements:
* Command-line version of gpg (check with `whereis gpg`)
* Access to localhost port 1717

#### Tested :

```
Linux NA 4.19.0-kali4-amd64 #1 SMP Debian 4.19.28-2kali1 (2019-03-18) x86_64 GNU/Linux
Linux NA 4.18.0-15-generic #16~18.04.1-Ubuntu SMP Thu Feb 7 14:06:04 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux
Linux NA 5.0.0-31-generic #33~18.04.1-Ubuntu SMP Tue Oct 1 10:20:39 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux
```

#### Untested :

```
Windows
```

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