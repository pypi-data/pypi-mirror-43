# Kaching

Sound effects for making test driven development a bit more fun.

Kaching plays a variety of sounds from computer games to signify the
beginning of a test run, a failure and a success.

To install:

```bash
$ apt-get install mplayer (or equivalent)
$ pip install kaching
```

Command line use:

```bash
$ kaching start
[ starting sound ]

$ kaching fail
[ failure sound ]

$ kaching win
[ passing test sound ]
```

Python API use::

```python
>>> import kaching
>>> kaching.start()
[ starting sound ]

>>> kaching.fail()
[ failure sound ]

>>> kaching.win()
[ passing test sound ]
```

Kaching requires mpg123 to be installed to make a sound although it won't
raise an exception / exit with status code > 0 if it isn't.

Sounds taken from : http://soundfxnow.com/
