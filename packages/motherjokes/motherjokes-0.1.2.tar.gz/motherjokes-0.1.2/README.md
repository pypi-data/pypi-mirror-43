motherjokes ![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg) [![Build Status](https://travis-ci.org/FFFEGO/motherjokes.svg?branch=master)](https://travis-ci.org/FFFEGO/motherjokes) 
===========  

Transform sentences into awesome jokes about your mother (in russian language for now).  

Installation
------------

```bash
pip install motherjokes
```

How to use
----------

```python
from motherjokes import MotherJokeGenerator

jokes = MotherJokeGenerator()
joke = jokes.get_joke('Я люблю шутить про мамок')
print(joke)
```

*Inspired by [rwge-discord](https://github.com/rwgeaston/rwge-discord)*
