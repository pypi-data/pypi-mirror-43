# cuisel

Cuisel is a ncurses-based tool that allows you to select a list of items iteractively on your terminal. It can also be used programmatically in Python.

# Installing from PyPI

```
$ pip install cuisel
```

# Usage

As a shell command:

[![asciicast](https://asciinema.org/a/236084.svg)](https://asciinema.org/a/236084)

As a Python package:

```
from cuisel import cuisel
selected = cuisel([i for i in range(1, 100)], modeline=True)
```

Please refer to the code for more detailed documentation.

# Shortcuts

Cuisel has a built-in VIM emulator which means you can move the cursor using 'j', 'k', 'G', etc. Here is the manual,

- [x] [count]j - move down
- [x] [count]k - move up
- [x] [count]G - move to row 'count' or bottom
- [x] [count]gg - move to row 'count' or top
- [x] u - deselect all items
- [x] v - enter batch mode
- [x] m/SPACE - select
- [ ] [count]zt,zz,zb - redraw
- [ ] CTRL-D,CTRL-Y,etc. - scroll window upwards/downwards
- [ ] / - search

As you can see, the supported features are quite limited. So feel free to send me a pull request.

