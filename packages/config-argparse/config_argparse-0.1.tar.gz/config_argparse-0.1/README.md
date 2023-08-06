# config_argparse

example

```
from config_argparse import Config, Value, DynamicConfig

class ConfigA(Config):
    a = 1

class ConfigB(Config):
    b = 1

config_map = {
    'a': ConfigA,
    'b': ConfigB,
}

class MyConfig(Config):
    lr = 0.1
    epoch = 100
    model = Value('a', choices=list(config_map.keys()))
    model_cfg = DynamicConfig(lambda c: config_map[c.model]())

args = MyConfig().parse_args(['--lr', '1', '--model', 'b', '--model_cfg.b', '100'])

```

TODO:

- add test of `Value`
- add `setup.py`
- upload to PyPI
