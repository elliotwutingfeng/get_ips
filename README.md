# get_ips

![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
[![Coveralls](https://img.shields.io/coverallsCoverage/github/elliotwutingfeng/get_ips?logo=coveralls&style=for-the-badge)](https://coveralls.io/github/elliotwutingfeng/get_ips?branch=main)
[![GitHub license](https://img.shields.io/badge/LICENSE-BSD--3--CLAUSE-GREEN?style=for-the-badge)](LICENSE)

Get IPv4 and IPv6 addresses of hostnames using [socket.getaddrinfo()](https://docs.python.org/3/library/socket.html#socket.getaddrinfo).

## Requirements

Python 3.8+

## Setup

```shell
python3 -m venv venv
venv/bin/python3 -m pip install --upgrade pip
venv/bin/python3 -m pip install -r requirements.txt
```

## Testing

```shell
venv/bin/python3 -m pytest --cov --cov-report html
```

## Usage

```shell
venv/bin/python3 main.py --input-file sample_urls.txt --output-file output.txt
```
