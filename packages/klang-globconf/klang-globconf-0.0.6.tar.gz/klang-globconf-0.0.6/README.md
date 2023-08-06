[![Build status](https://cloudpartners.visualstudio.com/MyFirstProject/_apis/build/status/2?branch=master)](https://cloudpartners.visualstudio.com/MyFirstProject/_build/latest?definitionId=2&branch=master)



# globconf

Creates a global configparser object, regardless of the project and module in need of it

## Getting Started
In project:
```
from globconf import config
# config will attempt to read local config.ini file if present - otherwise:

if 'important section' not in config.sections():
    config.read_string("""
    [important section]
    host = critical-system.com
    user = REST_USER
    pwd = REST_PASSWORD
    verify_ssl = false
    """)
# or config.read('some_other_config.ini')

# load class using globconf.config
```

In modules:
```
from globconf import config, verify_required_options
class module(object):
    def __init__(self):
        sec = 'service now'
        self.cfg = verify_required_options(sec, ['host', 'user', 'pwd'])
        if not self.cfg.getboolean('verify_ssl', fallback=True):
            import urllib3
            urllib3.disable_warnings(InsecureRequestWarning)
```

And your module is happy as long as someone has initialised the needed section in the global config.

### Prerequisites

configparser


### Installing

A step by step series of examples that tell you how to get a development env running


```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

### package

    python setup.py sdist


### test
    
    pytest
    
or
    
    pyton -m unittest

## Authors

* **Steffen Schumacher** - *Initial work* - [steffenschumacher](https://github.com/steffenschumacher)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
