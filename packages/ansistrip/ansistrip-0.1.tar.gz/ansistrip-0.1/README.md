# Ansistrip
*Module to strip ANSI Escape codes from a string.*

## Installation
### Install with pip
```
pip3 install -U ansistrip
```

## Usage
```
In [1]: import ansistrip

In [2]: text =  "\x1b[1m\x1b[38;5;10mtest\x1b0m"

In [3]: ansistrip.ansi_strip(text)

Out[3]: 'test'
```
