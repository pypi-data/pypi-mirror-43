# Tokenizer for text messages

## Setup

TODO

## Usage

```py
from tokenizer import Tokenizer

INPUT_STRING = '!bot create george'
tokens = Tokenizer(INPUT_STRING)
if tokens.match('!bot create <name>'):
  items = tokens.items()
  print('Name is: {}'.format(items['name']))
```

Note: `.items()` must be called after a `.match()`
