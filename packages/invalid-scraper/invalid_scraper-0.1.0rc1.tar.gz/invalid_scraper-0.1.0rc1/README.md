<!--description: A tool for finding rov-invalid received routes. -->
[![PyPI](https://img.shields.io/pypi/v/invalid-scraper.svg)](https://pypi.python.org/pypi/invalid-scraper)
[![Build Status](https://travis-ci.com/wolcomm/invalid-scraper.svg?branch=master)](https://travis-ci.com/wolcomm/invalid-scraper)
[![codecov](https://codecov.io/gh/wolcomm/invalid-scraper/branch/master/graph/badge.svg)](https://codecov.io/gh/wolcomm/invalid-scraper)

# invalid-scraper

Iterate through a list of Cisco IOS routers (`invalid_scraper/data/hosts.yml`)
and find RPKI Invalid routes learnt from neighbors.

## Usage

```
usage: invalid-scraper [-h] [--domain DOMAIN] [--username USERNAME]

optional arguments:
  -h, --help            show this help message and exit
  --domain DOMAIN, -d DOMAIN
  --username USERNAME, -u USERNAME
```

